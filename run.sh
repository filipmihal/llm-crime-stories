#!bin/bash

set -e

# Package.
if [ -d ".venv" ]; then
    echo "Removing old venv"
    rm -rf .venv
fi

python3 -m venv .venv
.venv/bin/pip install --upgrade pip setuptools
.venv/bin/pip install -e .
.venv/bin/pip install black isort autoflake

# Format.
.venv/bin/black src --target-version py310
.venv/bin/autoflake --in-place --remove-all-unused-imports --recursive src
.venv/bin/isort src --profile black

# Tests.
if [ -d ".venv-test" ]; then
    echo "Removing old test venv"
    rm -rf .venv-test
fi

python3 -m venv .venv-test
.venv-test/bin/pip install -U setuptools pip wheel
.venv-test/bin/pip install -e '.[tests]'
.venv-test/bin/pytest tests