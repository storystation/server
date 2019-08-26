#!/bin/sh

VENV_BIN=/home/vagrant/flask/venv/bin

if [ "$1" = "--debug" ]
then
  if [ "$(sudo systemctl is-active storystation)" = "active" ]; then
    echo "Stopping systemd instance of storystation server..."
    sudo systemctl stop storystation
  fi
  export FLASK_ENV=development
  export DEBUG="True"
  # gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" -b 127.0.0.1:3333 --reload --access-logfile "-" --log-level "debug" startup:__main__
else
  echo "" > /dev/null
  # gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" -b 127.0.0.1:3333 startup:app
fi

cd src

$VENV_BIN/python startup.py
