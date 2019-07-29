#!/bin/sh

. venv/bin/activate

export FLASK_APP=startup.py
export FLASK_ENV=development
export FLASK_BIN=/home/vagrant/flask/venv/bin
cd src
echo $(pwd)
$FLASK_BIN/flask run -p 3333 -h 0.0.0.0