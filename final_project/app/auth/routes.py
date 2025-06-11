from flask import render_template, redirect, url_for, flash
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)

@bp.route('/logout')
def logout():
    # Placeholder for logout logic
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))  # Redirect to login page after logout

