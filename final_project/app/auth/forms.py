from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from models import User
 
 
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    role = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Login')
    
    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(password.data):
            raise ValueError('Invalid password. Please try again.')
        if not user:
            raise ValueError('Email not registered. Please register first.')
        return user
    
    
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValueError('Email already registered. Please use a different email.')
        
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValueError('Username already taken. Please choose a different username.')
        
        