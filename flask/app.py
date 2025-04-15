from flask import Flask
import os
from models import db
from celery_config import celery_init_app

BASE_DIR = os.path.abspath(os.getcwd())
app = Flask(__name__)
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
    ),
)

celery_app = celery_init_app(app)


app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'books.db')}"

db.init_app(app=app)

with app.app_context():
    db.create_all()

from routes import *
from api import *

if __name__ == "__main__":
    app.run(debug=True)
        
