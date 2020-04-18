from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_session import Session
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_json('../h42auth-config.json')
app.config['SESSION_FILE_DIR'] = 'data/flask_session'
app.config['SESSION_TYPE'] = 'filesystem'
#app.config['MONGO_URI'] = 'mongodb://root:mysupersecret@192.168.1.64:27017/'
Bootstrap(app)
Session(app)
CORS(app)
mongo = PyMongo(app, connect=True)
login = LoginManager(app)

from h42auth import routes, user, forms, filters
