# Gitlab Registry Cleanup Hook

Listens for incoming requests and deletes docker images if merge request is merged.

## Install

```
cp env.example .env
docker-compose up -d
```

Create system hook from `/admin/hooks`
- URL: `http://this-service:8000/`
- Secret Token: same as `$HOOK_TOKEN` from the `.env`
- Trigger: Merge request events

## Customize images to delete

By default `IMAGE_NAME_TEMPLATE=%(project_path)s/branches:%(branch)s` is used to find images to delete.

It's a comma separated list of images to delete.

You can override this per project,
by setting [project custom attribute].

[project custom attribute]: https://docs.gitlab.com/ce/api/custom_attributes.html

```bash
# Project custom attribute name to set per project override for IMAGE_NAME_TEMPLATE
# https://docs.gitlab.com/ce/api/custom_attributes.html
IMAGE_NAME_PROJECT_ATTRIBUTE=gitlab_registry_image_template
```

This will configure to cleanup `branches:BRANCH_NAME-node-8` and `branch:BRANCH_NAME-node-10` images when MR is merged:
```bash
./set-project-attribute.sh gitlab-org/gitlab-ce '%(project_path)s/branches:%(branch)s-node-8,%(project_path)s/branches:%(branch)s-node-10'
{"key":"custom_attribute","value":"%(project_path)s/branches:%(branch)s-node-8,%(project_path)s/branches:%(branch)s-node-10"}
```

Invoking helper script without value, will delete the attribute:
```bash
./set-project-attribute.sh gitlab-org/gitlab-ce
```

## Credits

- [@morph027] for original [Python Gist]
- [@burnettk] for [delete_docker_registry_image.py]
- [@n0madic] for [gricleaner.py]

[@burnettk]: https://github.com/burnettk
[@morph027]: https://gitlab.com/morph027
[@n0madic]: https://gitlab.com/n0madic
[Python Gist]: https://gitlab.com/snippets/1091155/
[delete_docker_registry_image.py]: https://github.com/burnettk/delete-docker-registry-image
[gricleaner.py]: https://github.com/n0madic/gitlab-registry-images-cleaner
