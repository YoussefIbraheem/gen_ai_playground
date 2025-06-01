import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    # General Config
    SECRET_KEY = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv(f'sqlite:///{os.getenv("DB_NAME")}', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    