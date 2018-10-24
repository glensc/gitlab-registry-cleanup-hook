#!/usr/local/bin/python3 -u

#  Listens for incoming requests and deletes docker images if merge request is merged.
#
# You should also run registry garbage collection,
# either afterwards (might break your productive env) or at night (cronjob, better)
# $ gitlab-ctl registry-garbage-collect

from os import environ as env
from bottle import request, route, run, error, HTTPResponse
import requests
from gricleaner import GitlabRegistryClient
import logging
import json

logger = logging.getLogger(__name__)

# basic security, add this token to the project's webhook
# get one:
# < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c"${1:-32}";echo;
token = env.get('HOOK_TOKEN')

NoContentResponse = HTTPResponse(status=204)

class JsonResponse(HTTPResponse):
    def __init__(self, body={}, status=None, headers={}, **more_headers):
        headers['Content-Type'] = 'application/json'
        payload = json.dumps(body)
        super(HTTPResponse, self).__init__(payload, status, headers, **more_headers)


def createClient():
    user = env.get('GITLAB_USER')
    password = env.get('GITLAB_PASSWORD')
    jwt_url = env.get('GITLAB_JWT_URL')
    registry_url = env.get('GITLAB_REGISTRY')
    if None in [user, password, jwt_url, registry_url]:
        raise Exception('Some required env variable missing')

    authentication = (
        user,
        password,
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
    if request.get_header('X-GITLAB-TOKEN') != token:
        return NoContentResponse

    if not request.get_header('X-GITLAB-EVENT') in ["Merge Request Hook", "System Hook"]:
        return NoContentResponse

    data = request.json
    if 'event_type' not in data:
        return NoContentResponse
    if data['event_type'] != 'merge_request' or data['object_attributes']['state'] != 'merged':
        return NoContentResponse

    logger.info("Merge detected, processing")
    return cleanup(data)


def cleanup(data):
    branch = data['object_attributes']['source_branch']
    project_path = data['object_attributes']['source']['path_with_namespace']

    image = "%s/branches" % project_path
    tag = branch

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
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(u'%(levelname)-8s [%(asctime)s]  %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    client = createClient()
    run(host='0.0.0.0', port=8000)
