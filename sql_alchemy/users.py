from database import User , engine
from session import session

users = session.query(User).all()

for user in users:
    print(user)