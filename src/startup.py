import sys

from flask import Flask
from flask_mongoengine import MongoEngine

from Routes import Auth

app = Flask(__name__)
app.config.from_json('config_default.json')
app.config.from_json('config_user.json', True)
db = MongoEngine(app)

app.register_blueprint(Auth.bp)


@app.route('/')
def hello_world():
    return "Hello, World !"
