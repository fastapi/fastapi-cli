#!/bin/sh -e
set -x
set -e

ruff src tests scripts --fix
ruff format src tests scripts
