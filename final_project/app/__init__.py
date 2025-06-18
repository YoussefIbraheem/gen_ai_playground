from flask_sqlalchemy import SQLAlchemy
from flask import Flask , render_template , redirect, url_for
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
    
    @login.user_loader
    def load_user(user_id):
        from models import User  # Import User model here to avoid circular imports
        return User.query.get(int(user_id))
    
    
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.chat import bp as chat_bp
    app.register_blueprint(chat_bp)
    
    
    return app
    