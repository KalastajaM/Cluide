#!/usr/bin/env bash
# Fail-closed release check: does the remote tag peel to the remote trunk tip?
# Usage: verify-tag.sh <tag> [remote=origin] [branch=main]
# Exit: 0 RELEASED, 1 not released or could not verify.
set -uo pipefail
tag=${1:?usage: verify-tag.sh <tag> [remote] [branch]}; remote=${2:-origin}; branch=${3:-main}
T=$(git ls-remote "$remote" "refs/tags/$tag^{}" 2>/dev/null | cut -f1)
[ -z "$T" ] && T=$(git ls-remote "$remote" "refs/tags/$tag" 2>/dev/null | cut -f1)   # lightweight tag
M=$(git ls-remote "$remote" "refs/heads/$branch" 2>/dev/null | cut -f1)
if [ -n "$T" ] && [ -n "$M" ] && [ "$T" = "$M" ]; then
  echo "RELEASED $tag = $remote/$branch ($M)"; exit 0
fi
echo "NOT RELEASED (tag=${T:-<none>} $branch=${M:-<none>})"; exit 1
