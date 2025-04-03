from session import session
from database import User 

user = session.query(User).filter_by(name="Youssef").first()

user.age = 30

session.commit()