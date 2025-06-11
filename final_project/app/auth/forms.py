from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo , ValidationError
from models import User
 
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Login')
    
    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(password.data):
            raise ValidationError('Invalid password. Please try again.')
        if not user:
            raise ValidationError('Email not registered. Please register first.')
        return user
    
    
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = StringField('Role')
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')
        
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different username.')
    
    def validate_password(self, password):
        if len(password.data) < 6 or len(password.data) > 20:
            raise ValidationError('Password must be between 6 and 20 characters long.')
        return password
    
    def create_user(self):
        user = User(username=self.username.data, email=self.email.data, role=self.role.data or 'customer')
        user.set_password(self.password.data)
        user.create()
        return user
        
        