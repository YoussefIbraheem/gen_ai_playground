from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user , logout_user
from models import User
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.validate_password(form.password)
        if user:   
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to a protected route or home page
    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        redirect_url = url_for('auth.login')
        flash('Registration successful! You can now log in.', 'success')
        return redirect(redirect_url)
    return render_template('register.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))  # Redirect to login page after logout

