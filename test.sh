#!/bin/bash

set -x
set -e

cp -uv hooks/* .git/hooks

pylint rpn io_test.py
python io_test.py

