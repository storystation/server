from flask import Flask, request
from flask_mongoengine import MongoEngine
from Controller.UsersController import UsersController

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "host": "mongodb://localhost:27007/storystation",
    "db": "storystation",
}
db = MongoEngine(app)


@app.route('/')
def hello_world():
    return UsersController.show()


@app.route('/', methods=['POST'])
def create_user():
    return UsersController.store(req=request)
