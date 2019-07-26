from flask import Flask
from flask_mongoengine import MongoEngine

from Controller.UsersController import UsersController
from Routes import Auth

app = Flask(__name__)
app.config.from_json('config_default.json')
app.config.from_json('config_user.cfg', True)
db = MongoEngine(app)

app.register_blueprint(Auth.bp)


@app.route('/')
def hello_world():
    return UsersController.show()
