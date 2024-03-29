#!/usr/bin/env sh

export PYTHON_BIN=/home/vagrant/.pyenv/shims
export PYTHON_VENV_BIN=/home/vagrant/flask/venv/bin
export VENV_LIB_FOLDER=/home/vagrant/flask/venv/lib/python3.7/site-packages/

if [ ! -f $PYTHON_VENV_BIN/flask ] || [ ! -d $VENV_LIB_FOLDER/flask_mongoengine ]\
|| [ ! -d $VENV_LIB_FOLDER/jwt ] || [ ! -d $VENV_LIB_FOLDER/flask_cors ]\
|| [ ! -d $VENV_LIB_FOLDER/geventwebsocket ] || [ ! -d $VENV_LIB_FOLDER/gevent ]; then
    $PYTHON_BIN/python -m venv venv
    $PYTHON_BIN/python -m venv venv --copies

    echo "Installing packages..."
    $PYTHON_VENV_BIN/python -m pip install -r requirements.txt
fi

