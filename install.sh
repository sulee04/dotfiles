#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ "${1:-}" != --help && "${1:-}" != -h && " $* " != *" --dry-run "* ]]; then
  missing=()
  for tool in python3 git perl make tar unzip rg curl; do
    command -v "$tool" >/dev/null || missing+=("$tool")
  done
  [[ -r /usr/share/bash-completion/bash_completion || -r /etc/bash_completion ]] || missing+=(bash-completion)
  if ((${#missing[@]})); then
    if ! command -v apt-get >/dev/null; then
      echo "Install these prerequisites and rerun: ${missing[*]}" >&2
      exit 1
    fi
    elevate=()
    if ((EUID != 0)); then elevate=(sudo); fi
    "${elevate[@]}" apt-get update
    "${elevate[@]}" apt-get install -y python3 git perl make tar unzip ripgrep curl ca-certificates bash-completion
  fi
fi
exec python3 "$repo_dir/scripts/setup.py" "$@"
