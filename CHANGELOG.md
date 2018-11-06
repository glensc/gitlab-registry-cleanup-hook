# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2018-11-06

### Added
- Make image names configurable via template [#8], [#2]

[0.5.0]: https://github.com/glensc/gitlab-registry-cleanup-hook/compare/0.4.0...0.5.0
[#8]: https://github.com/glensc/gitlab-registry-cleanup-hook/pull/8
[#2]: https://github.com/glensc/gitlab-registry-cleanup-hook/issues/1

## [0.4.0] - 2018-11-04

### Added
- Added docker swarm example with secrets [#6]

### Changed
- `GITLAB_PASSWORD` env is renamed to `GITLAB_TOKEN`
- Skip projects without Registry enabled [#7], [#3]

[0.4.0]: https://github.com/glensc/gitlab-registry-cleanup-hook/compare/0.3.0...0.4.0
[#7]: https://github.com/glensc/gitlab-registry-cleanup-hook/pull/7
[#6]: https://github.com/glensc/gitlab-registry-cleanup-hook/pull/6
[#3]: https://github.com/glensc/gitlab-registry-cleanup-hook/issues/3

## [0.3.0] - 2018-10-25

### Changed
- Use api to delete images, no longer requiring direct docker registry filesystem access [#1], [#5]

[0.3.0]: https://github.com/glensc/gitlab-registry-cleanup-hook/compare/0.2.1...0.3.0
[#5]: https://github.com/glensc/gitlab-registry-cleanup-hook/pull/5
[#1]: https://github.com/glensc/gitlab-registry-cleanup-hook/issues/1

## [0.2.1] - 2018-10-15

### Fixed
- Workaround for [gitlab-ce#52672] sending wrong events to the hook

[0.2.1]: https://github.com/glensc/gitlab-registry-cleanup-hook/compare/0.2.0...0.2.1
[gitlab-ce#52672]: https://gitlab.com/gitlab-org/gitlab-ce/issues/52672

## [0.2.0] - 2018-10-13

### Added
- Add `Dockerfile`, `docker-compose.yml`.
- Load Hook token from `$HOOK_TOKEN` environment variable.
- Support setup as System Hook

[0.2.0]: https://github.com/glensc/gitlab-registry-cleanup-hook/compare/0.1.0...0.2.0

## [0.1.0] - 2018-10-13

### Added
- Add Gitlab Registry Cleanup Hook (Python) snippet from https://gitlab.com/snippets/1091155/

[0.1.0]: https://github.com/glensc/gitlab-registry-cleanup-hook/commits/0.1.0
