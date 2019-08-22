#!/bin/sh

. venv/bin/activate

export FLASK_APP=startup.py
export FLASK_ENV=development
export FLASK_BIN=/home/vagrant/flask/venv/bin

cd src

if [ "$1" = "--debug" ]
then
  if [ "$(sudo systemctl is-active storystation)" = "active" ]; then
    echo "Stopping systemd instance of storystation server..."
    sudo systemctl stop storystation
  fi
  export DEBUG="True"
  python startup.py
else
  gunicorn -k flask_sockets.worker -b 127.0.0.1:3333 startup:app
fi
