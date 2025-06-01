from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    role = db.Column(db.String(20), default='customer')
    
    chat_sessions = db.relationship('ChatSession', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')
        
    def check_password(self, password):
        return Bcrypt().check_password_hash(self.password, password)
    
    def has_access_to_table(self, table_name):
        role_permissions = {
            'admin': ['users', 'products', 'orders','categories','chat_sessions','orders_items','customers'],
            'manager': ['products', 'orders', 'categories','customers','users'],
            'customer': ['orders', 'products', 'categories'],
        }
        return table_name in role_permissions.get(self.role, [])
    
    
class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    
    user = db.relationship('User', backref=db.backref('chat_sessions', lazy=True))