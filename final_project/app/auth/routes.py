from flask import render_template, redirect, url_for, flash
from app.auth import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Placeholder for login logic
    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Placeholder for registration logic
    return render_template('register.html')

@bp.route('/logout')
def logout():
    # Placeholder for logout logic
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))  # Redirect to login page after logout

