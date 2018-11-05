#!/usr/local/bin/python3 -u

#  Listens for incoming requests and deletes docker images if merge request is merged.
#
# You should also run registry garbage collection,
# either afterwards (might break your productive env) or at night (cronjob, better)
# $ gitlab-ctl registry-garbage-collect

from os import environ
from bottle import request, route, run, HTTPResponse
import requests
from gricleaner import GitlabRegistryClient
import logging
import json
import gitlab


class JsonResponse(HTTPResponse):
    def __init__(self, body={}, status=None, headers={}, **more_headers):
        headers['Content-Type'] = 'application/json'
        payload = json.dumps(body)
        super(HTTPResponse, self).__init__(payload, status, headers, **more_headers)


class Config:
    def __init__(self):
        self.env = environ

    def get(self, name, default=None):
        if name == 'GITLAB_TOKEN':
            return self.get_secret(name)
        if name == 'HOOK_TOKEN':
            return self.get_secret(name)

        return self.env.get(name, default)

    def get_secret(self, name):
        secret_file = self.env.get('{}_FILE'.format(name))
        if secret_file is not None:
            secret = open(secret_file, 'r').read().splitlines()[0]
        else:
            secret = self.env.get(name)

        return secret

    def __getattr__(self, item):
        return self.get(item)


NoContentResponse = HTTPResponse(status=204)


def gitlabClient():
    api_url = config.get('GITLAB_API_URL')
    gl = gitlab.Gitlab(api_url, private_token=config.get('GITLAB_TOKEN'))
    logger.info("GitLab API: %s" % (api_url))

    return gl


def createClient():
    user = config.get('GITLAB_USER')
    token = config.get('GITLAB_TOKEN')
    jwt_url = config.get('GITLAB_JWT_URL')
    registry_url = config.get('GITLAB_REGISTRY')
    if None in [user, token, jwt_url, registry_url]:
        raise Exception('Some required env variable missing')

    authentication = (
        user,
        token,
    )
    registry_url = 'https://' + registry_url if not registry_url.startswith('http') else registry_url

    logger.info("Registry: %s, JWT: %s, User: %s" % (registry_url, jwt_url, user))

    return GitlabRegistryClient(
        auth=authentication,
        jwt=jwt_url,
        registry=registry_url
    )


@route('/', method='POST')
def validate():
    if request.get_header('X-GITLAB-TOKEN') != hook_token:
        return NoContentResponse

    if not request.get_header('X-GITLAB-EVENT') in ["Merge Request Hook", "System Hook"]:
        return NoContentResponse

    data = request.json
    if 'event_type' not in data:
        return NoContentResponse
    if data['event_type'] != 'merge_request' or data['object_attributes']['state'] != 'merged':
        return NoContentResponse

    logger.info("Merge detected, processing")
    project_id = data['project']['id']
    project = gl.projects.get(project_id)

    if not project.attributes['container_registry_enabled']:
        logger.info("Registry not enabled; skip")
        return NoContentResponse

    return cleanup(data)


def get_image_delete_list(project, data):
    image_template = config.get('IMAGE_NAME_TEMPLATE', '%(project_path)s/branches:%(branch)s')
    project_attribute = config.get('IMAGE_NAME_PROJECT_ATTRIBUTE')
    if project_attribute:
        # https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html#project-custom-attributes
        try:
            # https://python-gitlab.readthedocs.io/en/stable/api/gitlab.v4.html#gitlab.v4.objects.ProjectCustomAttribute
            attribute = project.customattributes.get(project_attribute)
            # https://python-gitlab.readthedocs.io/en/stable/api/gitlab.v4.html#gitlab.v4.objects.ProjectCustomAttribute
            image_template = attribute.value
        except gitlab.exceptions.GitlabGetError:
            pass

    attributes = {
        'branch': data['object_attributes']['source_branch'],
        'project_path': data['object_attributes']['source']['path_with_namespace'],
    }

    for template in image_template.split(','):
        image, tag = (template % attributes).split(':')
        yield image, tag


def cleanup(data):
    project_id = data['project']['id']
    project = gl.projects.get(project_id)

    for image, tag in get_image_delete_list(project, data):
        try:
            logger.info("Trying to delete %s:%s" % (image, tag))
            digest = client.get_digest(image, tag)
            if digest == None:
                logger.info("Image not present")
                return JsonResponse({'error': 'Image not found'}, status=404)

            result = client.delete_image(image, tag)
            if result:
                logger.info("Deleted %s:%s" % (image, tag))
                return JsonResponse({'status': 'Image deleted'}, status=200)

            logger.info("Image not deleted")
            return JsonResponse({'status': 'Image not deleted'}, status=202)

        except requests.exceptions.HTTPError as error:
            logger.fatal(error)
            return JsonResponse({'error': 'Underlying HTTP error. Details not disclosed.'}, status=500)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(u'%(levelname)-8s [%(asctime)s]  %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    config = Config()
    hook_token = config.get('HOOK_TOKEN')
    client = createClient()
    gl = gitlabClient()
    run(host='0.0.0.0', port=8000)
