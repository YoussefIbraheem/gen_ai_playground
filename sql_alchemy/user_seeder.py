from database import Post, User , Comment, Group, user_group
from session import session


user_1 = User(name="Youssef",age=29,email="xx@xx.com",password="123456")
user_2 = User(name="mohamed",age=32,email="xxe@xxe.com",password="123456")

session.add_all([
    user_1,\
    user_2
])

# post_1 = Post(title="my first post",content="this is my first post",user_id=1)
# post_2 = Post(title="my second post",content="this is my second post",user_id=2)
# session.add_all([
#     post_1,\
#     post_2
# ])
# comment_1 = Comment(content="this is my first comment",post_id=1,user_id=1)
# comment_2 = Comment(content="this is my second comment",post_id=2,user_id=2)
# session.add_all([
#     comment_1,\
#     comment_2
# ]) 
# group_1 = Group(name="my first group",description="this is my first group")
# group_2 = Group(name="my second group",description="this is my second group")
# session.add_all([
#     group_1,\
#     group_2
# ])
# user_group_1 = user_group(user_id=1,group_id=1)
# user_group_2 = user_group(user_id=2,group_id=2)
# session.add_all([
#     user_group_1,\
#     user_group_2
# ])



session.commit()
print(f"imporeted successfully")