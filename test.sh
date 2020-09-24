#!/bin/bash

set -x
set -e

cp -uv hooks/* .git/hooks
./rpn '???' > README.md

README_CHANGED=$(git status -s | grep -e '^ M README.md' || true)
[[ -z "$README_CHANGED" ]] || git add README.md

if [[ -n "$(git status -s | grep -e '^?? |^ M ')" && ( "$UNCOMMITTED" != "Y" ) ]]; then
  git status
  echo 'You have uncommitted files, set UNCOMMITTED=Y to force.'
  exit 1
fi

CHANGED_FILES=$(git status -s | grep -e '[rpn|\.py]$' | awk '{ print $2 }' || true)
[[ -z "$CHANGED_FILES" ]] || pylint $CHANGED_FILES
python io_test.py

