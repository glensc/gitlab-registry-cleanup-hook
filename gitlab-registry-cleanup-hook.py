#!/usr/bin/env python

#
# Disclaimer: Dirty workaround, i'm not responsible for anything, although it works for us
#
# simple webhook script for https://gitlab.com/gitlab-org/gitlab-ce/issues/21608#note_22185264
# uses https://github.com/burnettk/delete-docker-registry-image
#
# listens on POST requests containing JSON data from Gitlab webhook (on merge)
# it uses bottlepy, so setup like:
#   pip install bottle
# you can run it like
#   nohup /opt/registry-cleanup/python/registry-cleaner.py >> /var/log/registry-cleanup.log 2>&1 &
# also you need to put delete-docker-registry-image into the same directory:
#   curl -O https://raw.githubusercontent.com/burnettk/delete-docker-registry-image/master/delete_docker_registry_image.py
#
# you should also run registry garbage collection, either afterwards (might break your productive env) or at night (cronjob, better)
# gitlab-ctl registry-garbage-collect

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
    if request.get_header('X-GITLAB-EVENT') == "Merge Request Hook" and request.get_header('X-GITLAB-TOKEN') == token:
      logger.info("Valid request, processing")
      cleanup()

def cleanup():
    data = request.json
    state = data['object_attributes']['state']
    if state != 'merged':
        return

    logger.info("Merge detected")
    branch = data['object_attributes']['source_branch']
    path_with_namespace = data['object_attributes']['source']['path_with_namespace'].split("/")
    project_namespace =  path_with_namespace[0]
    project_name = path_with_namespace[1]
    registry_data_dir = "/var/opt/gitlab/gitlab-rails/shared/registry/docker/registry/v2"
    image = "%s/%s" % ( project_namespace, project_name )
    tag = branch
    dry_run = False
    untagged = False
    prune = True

    logger.info("Trying to delete %s:%s" %( image, branch ))

    try:
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
