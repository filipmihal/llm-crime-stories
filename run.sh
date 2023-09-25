#!/bin/bash

set -e

if conda env list | grep -q venv; then
    echo "Removing old main environment"
    conda env remove -n venv -y
fi

conda create -n venv -y python=3.10

VENV_PATH=$(conda info --envs | grep venv | sed 's/ \+/ /g' | cut -d " " -f2)

conda install --prefix $VENV_PATH pip setuptools -y
$VENV_PATH/bin/pip install -e .

# Install additional packages.
$VENV_PATH/bin/pip install black black[jupyter] isort autoflake

# Format code.
$VENV_PATH/bin/black src --target-version py310
$VENV_PATH/bin/autoflake --in-place --remove-all-unused-imports --recursive src
$VENV_PATH/bin/isort src --profile black