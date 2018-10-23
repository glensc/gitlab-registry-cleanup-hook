#!/usr/local/bin/python3 -u

#  Listens for incoming requests and deletes docker images if merge request is merged.
#
# You should also run registry garbage collection,
# either afterwards (might break your productive env) or at night (cronjob, better)
# $ gitlab-ctl registry-garbage-collect

from os import environ as env
from bottle import request, route, run
import delete_docker_registry_image
import logging

logger = logging.getLogger(__name__)

# basic security, add this token to the project's webhook
# get one:
# < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c"${1:-32}";echo;
token = env.get('HOOK_TOKEN')


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
    registry_data_dir = "/var/opt/gitlab/gitlab-rails/shared/registry/docker/registry/v2"
    image = "%s/branches" % project_path
    tag = branch
    dry_run = False
    untagged = False
    prune = True

    try:
        logger.info("Trying to delete %s:%s" % (image, branch))
        cleaner = delete_docker_registry_image.RegistryCleaner(registry_data_dir, dry_run)
        if untagged:
            cleaner.delete_untagged(image)
        else:
            if tag:
                cleaner.delete_repository_tag(image, tag)
            else:
                cleaner.delete_entire_repository(image)

        if prune:
            cleaner.prune()
        logger.info("Deleted %s:%s" % (image, branch))
    except delete_docker_registry_image.RegistryCleanerError as error:
        logger.fatal(error)


def main():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(u'%(levelname)-8s [%(asctime)s]  %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    run(host='0.0.0.0', port=8000)


if __name__ == "__main__":
    main()
