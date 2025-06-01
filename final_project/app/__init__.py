from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, ForeignKey , Text
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime
from flask import Flask

db = SQLAlchemy()
