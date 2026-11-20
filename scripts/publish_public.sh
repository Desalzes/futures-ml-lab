#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" != "--confirm-public" ]]; then
  echo 'Refusing to publish. Review the files and run: bash scripts/publish_public.sh --confirm-public' >&2
  exit 2
fi
cd "$(dirname "$0")/.."
if [[ -d .git ]]; then
  echo 'This folder already contains a .git directory. Refusing to alter its history.' >&2
  exit 3
fi
command -v gh >/dev/null || { echo 'Install and authenticate GitHub CLI (gh).' >&2; exit 4; }
command -v git >/dev/null || { echo 'git is required.' >&2; exit 4; }
gh auth status >/dev/null || { echo 'Run gh auth login.' >&2; exit 4; }
if gh repo view Desalzes/futures-ml-lab >/dev/null 2>&1; then
  echo 'Repository already exists. Review and publish manually.' >&2
  exit 5
fi
printf '%s\n' 'You are about to create a PUBLIC repository from these exact files:'
find . -type f -not -path './.git/*' -not -path './.venv/*' | sort
printf '%s' 'Type PUBLIC to proceed: '
read -r confirmation
[[ "$confirmation" == "PUBLIC" ]] || { echo 'Cancelled.'; exit 6; }
git init -b main
git add .
git commit -m 'Initial public bar-only ML research lab'
gh repo create Desalzes/futures-ml-lab --public --source=. --remote=origin --push
printf '%s\n' 'Created: https://github.com/Desalzes/futures-ml-lab'
