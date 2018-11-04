# Gitlab Registry Cleanup Hook

## [0.4.0] - 2018-11-04

NOTE: `GITLAB_PASSWORD` env is renamed to `GITLAB_TOKEN`

- Added docker swarm example with secrets [#6]
- Skip projects without Registry enabled [#7], [#3]

[0.4.0]: https://github.com/glensc/gitlab-registry-cleanup-hook/compare/0.3.0...0.4.0
[#7]: https://github.com/glensc/gitlab-registry-cleanup-hook/pull/7
[#6]: https://github.com/glensc/gitlab-registry-cleanup-hook/pull/6
[#3]: https://github.com/glensc/gitlab-registry-cleanup-hook/issues/3

## [0.3.0] - 2018-10-25

- Use api to delete images, no longer requiring direct docker registry filesystem access [#1], [#5]

[0.3.0]: https://github.com/glensc/gitlab-registry-cleanup-hook/compare/0.2.1...0.3.0
[#5]: https://github.com/glensc/gitlab-registry-cleanup-hook/pull/5
[#1]: https://github.com/glensc/gitlab-registry-cleanup-hook/issues/1

## [0.2.1] - 2018-10-15

- Workaround for [gitlab-ce#52672] sending wrong events to the hook

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
