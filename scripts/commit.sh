#!/usr/bin/env bash
# Commit and push changed files, retrying if another run pushed first.
set -euo pipefail
msg="$1"; shift
git config user.name "job-radar-bot"
git config user.email "job-radar-bot@users.noreply.github.com"
for f in "$@"; do if [ -e "$f" ]; then git add "$f"; fi; done
if git diff --cached --quiet; then
  echo "nothing to commit"; exit 0
fi
git commit -q -m "$msg"
for i in 1 2 3 4 5; do
  if git pull -q --rebase origin main && git push -q origin HEAD:main; then
    echo "pushed"; exit 0
  fi
  sleep $((i * 3))
done
echo "push failed after retries" >&2
exit 1
