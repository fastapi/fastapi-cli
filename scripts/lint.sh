#!/usr/bin/env bash

set -e
set -x

mypy src tests
ty check src tests
ruff check src tests scripts
ruff format src tests --check
