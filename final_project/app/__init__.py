from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
socketio = SocketIO()
bcrypt = Bcrypt()
login = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    login.init_app(app)
    login.login_view = 'auth.login'
    bcrypt.init_app(app)
    
    return app
    