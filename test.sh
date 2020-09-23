#!/bin/bash

set -x
set -e

cp -uv hooks/* .git/hooks
./rpn '???' > README.md

CHANGED_FILES=$(git status -s | grep -e '[rpn|\.py]$' | awk '{ print $2 }')
[[ -z "$CHANGED_FILES" ]] || pylint $CHANGED_FILES
python io_test.py

