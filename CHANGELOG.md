# Gitlab Registry Cleanup Hook

## [0.3.0] - 2018-10-25

- use api to delete images, no longer requiring direct docker registry filesystem access [#5]

[0.3.0]: https://github.com/glensc/gitlab-registry-cleanup-hook/compare/0.2.1...0.3.0
[#5]: https://github.com/glensc/gitlab-registry-cleanup-hook/pull/5

## [0.2.1] - 2018-10-15

- payload: ensure the key exists what is compared. workaround for [gitlab-ce#52672]

[0.2.1]: https://github.com/glensc/gitlab-registry-cleanup-hook/compare/0.2.0...0.2.1
[gitlab-ce#52672]: https://gitlab.com/gitlab-org/gitlab-ce/issues/52672

## [0.2.0] - 2018-10-13

- Add `Dockerfile`, `docker-compose.yml`.
- Load Hook token from `$HOOK_TOKEN` environment variable.
- Support setup as System Hook

[0.2.0]: https://github.com/glensc/gitlab-registry-cleanup-hook/compare/0.1.0...0.2.0

## [0.1.0] - 2018-10-13

- Add Gitlab Registry Cleanup Hook (Python) snippet from https://gitlab.com/snippets/1091155/

[0.1.0]: https://github.com/glensc/gitlab-registry-cleanup-hook/commits/0.1.0
