#!/bin/sh -e
set -x
set -e

ruff check src tests scripts --fix
ruff format src tests scripts
