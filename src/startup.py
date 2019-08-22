from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS

from Routes import Auth, Story


app = Flask(__name__)
app.config.from_json('config_default.json')
app.config.from_json('config_user.json', True)
cors = CORS(app, send_wildcard=True)

db = MongoEngine(app)

app.register_blueprint(Auth.bp)
app.register_blueprint(Story.bp)


@app.route('/')
def hello_world():
    return "Hello, World !"
