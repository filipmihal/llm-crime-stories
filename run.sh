#!bin/bash

set -e

if [ -d "./venv" ]; then
    echo "Removing old venv"
    rm -rf ./venv
fi

python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
