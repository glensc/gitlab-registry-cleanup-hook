# Gitlab Registry Cleanup Hook

Listens for incoming requests and deletes docker images if merge request is merged.

## Install

```
cp env.example .env
docker-compose up -d
```

Create system hook from `/admin/hooks`
- URL: http://this-service:8000/
- Secret Token: same as `$HOOK_TOKEN` from the `.env`
- Trigger: Merge request events

## Credits

- [@morph027] for original [Python Gist]
- [@burnettk] for [delete_docker_registry_image.py]

[@burnettk]: https://github.com/burnettk
[@morph027]: https://gitlab.com/morph027
[Python Gist]: https://gitlab.com/snippets/1091155/
[delete_docker_registry_image.py]: https://github.com/burnettk/delete-docker-registry-image
