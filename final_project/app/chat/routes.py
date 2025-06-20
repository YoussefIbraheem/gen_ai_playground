from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user , logout_user , login_required
from models import User
from app import db , socketio
from app.chat import bp
from app.chat.ai import initialize_sql_agent


@login_required
@bp.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat/chat.html')


@login_required
@socketio.on('sending-message')
def handle_send_message(data):
    message = data['message']
    print(f"Received message: {message}")
    agent = initialize_sql_agent()
    response = agent.invoke({"input": message})
    socketio.emit('receive-message', {'message': response['output']})
