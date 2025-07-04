from app import create_app, db, socketio

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    socketio.run(app,debug=True, host='0.0.0.0', port=5000)  # Run the Flask app with SocketIO support