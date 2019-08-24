# Storystation API and webserver

This project contains the whole server-side logic to make storystation (prototype) a thing. It implements an HTTP and a Websocket server to interact with the website and the Raspberry board.

This is a Python project with [flask](https://github.com/pallets/flask/)

## Setup

```
git clone https://github.com/storystation/server.git storystation_server
cd storystation_server

python -m venv venv
. venv/bin/activate

./setup.sh
```

The server needs a mongo database. Fill the src/config_default.json file with proper DB connection info 

## Dev server

```
cd storystation_server

./run.sh --debug
```

The server runs locally on 127.0.0.1:3333.

---

## Runs the dev server into a vagrant instance

The project has a Vagrantfile provisioning a centos 7 box. The script installs git, docker, pyenv and sets the flask dev server into systemd. The project folder is synced into `~/flask`. Once the provision is done (approx 7 mins), the server must be available on the vagrant box's public ip, port 80.

### Troubleshooting

- The flask server `systemd` task can fails in multiple ways. If the service is not started, try `systemctl restart storystation.service` until it's properly activated.
- If the setup.sh script fails, try running `pip install` explicitely from the server's venv with `venv/bin/python -m pip install -r requirements.txt`
- The centos 7 box from roboxes has a specific iptables config loaded at startup. You must allow inputs to port 3333. In doubt, you can run that function from the provisioning script: `iptables -D INPUT -j REJECT --reject-with icmp-host-prohibited`
- On vagrant up, a provisioning script starts storystation systemd service. To launch the debug server, you must `sudo systemctl stop storystation` and launch `~/home/flask/run.sh --debug`
- You must be sure you python version is correct. If your systemd reports weird python errors, try reinstalling your global python version with pyenv. Also try resetting your venv in `~/flask` 