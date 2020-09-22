#!/bin/bash

set -x
set -e

cp -uv hooks/* .git/hooks

pylint rpn


