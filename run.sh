#!/bin/sh

. ../venv/bin/activate

export FLASK_APP=startup.py
export FLASK_ENV=development
cd src
flask run -p 3333 -h 0.0.0.0