#!/usr/bin/env sh

export PYTHON_BIN=/home/vagrant/.pyenv/shims
export PYTHON_VENV_BIN=/home/vagrant/flask/venv/bin

if [[ ! -f $PYTHON_VENV_BIN/flask ]]; then
    $PYTHON_BIN/python -m venv venv --copies
    . venv/bin/activate

    $PYTHON_VENV_BIN/pip install -r requirements.txt
fi

