import os
import signal

import gevent
from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from geventwebsocket import WebSocketServer, Resource
from werkzeug.debug import DebuggedApplication

from Routes import Auth, Story
from Sockets import Game

app = Flask(__name__)
app.config.from_json('config_default.json')
app.config.from_json('config_user.json', True)
app.config['DEBUG'] = os.environ.get('DEBUG', False)
cors = CORS(app, send_wildcard=True)
db = MongoEngine(app)
greenletsPool = {}

app.register_blueprint(Auth.bp)
app.register_blueprint(Story.bp)


@app.route('/')
def hello_world():
    return "Hello, World !"


if __name__ == "__main__":
    from gevent import monkey
    monkey.patch_all()

    debug = 'DEBUG' in os.environ and os.environ['DEBUG'] == "True"
    WebSocketServer(
        ('127.0.0.1', 3333),
        Resource([
            ('^/ws/game', Game.GameSocketHandler),
            ('^/.*', DebuggedApplication(app))
        ]),

        debug=debug
    ).serve_forever()

    gevent.signal(signal.SIGQUIT, gevent.kill)
