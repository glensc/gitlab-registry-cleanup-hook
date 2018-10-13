# gitlab-registry-cleanup-hook

Gitlab Registry Cleanup Hook

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
