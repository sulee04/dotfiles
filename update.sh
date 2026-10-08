#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
case "${1:-}" in --help|-h) exec "$repo_dir/install.sh" --help ;; esac
if [[ " $* " != *" --no-pull "* && " $* " != *" --dry-run "* ]]; then
  if [[ -n "$(git -C "$repo_dir" status --porcelain)" ]]; then
    echo 'Commit or stash dotfile changes before updating, or use --no-pull.' >&2
    exit 1
  fi
  if git -C "$repo_dir" rev-parse --abbrev-ref '@{upstream}' >/dev/null 2>&1; then
    git -C "$repo_dir" pull --ff-only
  else
    echo 'No Git upstream configured; updating tools and applying local configs.'
  fi
fi
exec "$repo_dir/install.sh" --update "$@"
