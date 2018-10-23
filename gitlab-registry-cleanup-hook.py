#!/usr/local/bin/python3 -u

#  Listens for incoming requests and deletes docker images if merge request is merged.
#
# You should also run registry garbage collection,
# either afterwards (might break your productive env) or at night (cronjob, better)
# $ gitlab-ctl registry-garbage-collect

from os import environ as env
from bottle import request, route, run
import requests
from gricleaner import GitlabRegistryClient
import logging

logger = logging.getLogger(__name__)

# basic security, add this token to the project's webhook
# get one:
# < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c"${1:-32}";echo;
token = env.get('HOOK_TOKEN')


def createClient():
    authentication = (
        env.get('GITLAB_USER'),
        env.get('GITLAB_PASSWORD')
    )
    jwt_url = env.get('GITLAB_JWT_URL')
    registry_url = env.get('GITLAB_REGISTRY')
    registry_url = 'https://' + registry_url if not registry_url.startswith('http') else registry_url

    return GitlabRegistryClient(
        auth=authentication,
        jwt=jwt_url,
        registry=registry_url
    )


@route('/', method='POST')
def validate():
    if request.get_header('X-GITLAB-TOKEN') != token:
        return

    if not request.get_header('X-GITLAB-EVENT') in ["Merge Request Hook", "System Hook"]:
        return

    data = request.json
    if 'event_type' not in data:
        return
    if data['event_type'] != 'merge_request' or data['object_attributes']['state'] != 'merged':
        return

    logger.info("Merge detected, processing")
    cleanup(data)


def cleanup(data):
    branch = data['object_attributes']['source_branch']
    project_path = data['object_attributes']['source']['path_with_namespace']

    image = "%s/branches" % project_path
    tag = branch

    try:
        logger.info("Trying to delete %s:%s" % (image, tag))
        client.delete_image(image, tag)
        logger.info("Deleted %s:%s" % (image, tag))
    except requests.exceptions.HTTPError as error:
        logger.fatal(error)


if __name__ == "__main__":
    client = createClient()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(u'%(levelname)-8s [%(asctime)s]  %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    run(host='0.0.0.0', port=8000)
