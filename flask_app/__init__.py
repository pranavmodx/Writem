from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a500392d4394d86f885845600e33d3ca'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)
Bootstrap(app)
datepicker(app)

from flask_app import routes


