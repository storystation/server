import os

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask_sockets import Sockets

from Routes import Auth, Story


app = Flask(__name__)
app.config.from_json('config_default.json')
app.config.from_json('config_user.json', True)
app.config['DEBUG'] = os.environ.get('DEBUG', False)
cors = CORS(app, send_wildcard=True)
sockets = Sockets(app)

db = MongoEngine(app)

app.register_blueprint(Auth.bp)
app.register_blueprint(Story.bp)


@app.route('/')
def hello_world():
    return "Hello, World !"


@sockets.route('/ws/test')
def echo_socket(socket):
    while not socket.closed:
        message = socket.receive()
        socket.send(message)


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    import logging

    logging.basicConfig(level=logging.DEBUG)

    server = pywsgi.WSGIServer(('127.0.0.1', 3333), app, handler_class=WebSocketHandler, log=logging.Logger)
    server.serve_forever()
