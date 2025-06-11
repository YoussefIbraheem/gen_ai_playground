from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user , logout_user
from models import User
from app.chat import bp



@bp.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        # Handle chat message submission
        message = request.form.get('message')
        if message:
            # Here you would typically handle the message, e.g., save it to the database or process it
            flash('Message sent!', 'success')
        else:
            flash('Please enter a message.', 'danger')
    return render_template('chat/chat.html')