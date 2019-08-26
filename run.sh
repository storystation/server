#!/bin/sh

. venv/bin/activate

cd src

if [ "$1" = "--debug" ]
then
  if [ "$(sudo systemctl is-active storystation)" = "active" ]; then
    echo "Stopping systemd instance of storystation server..."
    sudo systemctl stop storystation
  fi
  export FLASK_ENV=development
  export DEBUG="True"
  python startup.py
else
  gunicorn -k flask_sockets.worker -b 127.0.0.1:3333 startup:app
fi
