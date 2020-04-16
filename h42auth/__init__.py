from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_session import Session
from flask_cors import CORS
from tinydb import TinyDB

app = Flask(__name__)
app.config.from_json('../h42auth-config.json')
app.config['SESSION_FILE_DIR'] = 'data/flask_session'
Bootstrap(app)
Session(app)
CORS(app)
login = LoginManager(app)
tydb = TinyDB('data/h42auth-data.db')

from h42auth import routes, user, forms
