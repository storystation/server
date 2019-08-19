#!/usr/bin/env sh

python -m venv venv --copies
. venv/bin/activate

pip install -r requirements.txt
