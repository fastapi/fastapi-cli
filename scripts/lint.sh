#!/usr/bin/env bash

set -e
set -x

mypy src tests scripts
ruff check src tests scripts
ruff format src tests --check
