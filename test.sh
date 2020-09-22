#!/bin/bash

set -x
set -e

cp -uv hooks/* .git/hooks

pylint rpn *.py
python io_test.py

