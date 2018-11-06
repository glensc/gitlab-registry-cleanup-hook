#!/bin/sh
#
# This script is part of https://github.com/glensc/gitlab-registry-cleanup-hook
# Author: Elan Ruusamäe <glen@pld-linux.org>
#
# Set project custom attribute:
# https://docs.gitlab.com/ce/api/custom_attributes.html

set -eu

die() {
	echo >&2 "$0: $*"
	exit 1
}

# need to load it with grep, because it's not shell syntax compatible
load_env() {
	local file="$1" t name value
	t=$(mktemp)

	grep '^[^#]' $file > $t
	while read line; do
		name=${line%%=*}
		value=${line#*=}
		eval "$name='$value'"
	done < $t
	rm -f $t
}

# load .env if present
test -e .env && load_env .env

project=$(echo "${1:-}" | sed -e 's;/;%2f;g')
value="${2:-}"

test -n "$project" || die "Usage: $0 project_id/project_path [value]"
test -n "$GITLAB_TOKEN" || die "GITLAB_TOKEN missing"
test -n "$GITLAB_API_URL" || die "GITLAB_API_URL missing"
test -n "$IMAGE_NAME_PROJECT_ATTRIBUTE" || die "IMAGE_NAME_PROJECT_ATTRIBUTE missing"

# if value is empty, delete the attribute
if [ -n "$value" ]; then
	set -- --request PUT --data-urlencode "value=$value"
else
	set -- --request DELETE
fi

set -- "$@" --header "Private-Token: $GITLAB_TOKEN" "$GITLAB_API_URL/api/v4/projects/$project/custom_attributes/$IMAGE_NAME_PROJECT_ATTRIBUTE"
exec curl "$@"
