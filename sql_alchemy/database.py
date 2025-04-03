from sqlalchemy import create_engine , Column , String , Integer , Date , Text , ForeignKey , Table
from sqlalchemy.orm import declarative_base , relationship


engine = create_engine("sqlite:///my_database.db")
connection = engine.connect()
print("connected to SQLite!")

Base = declarative_base()

user_group = Table(
    "user_group",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True)
)
                    
           

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer , primary_key=True)
    name = Column(String , nullable=False)
    age = Column(Integer, nullable= False)
    email = Column(String , unique= True)
    password = Column(String , nullable=False)
    
    posts = relationship("Post" , back_populates="user",cascade="all, delete-orphan")
    comments = relationship("Comment",back_populates="user",cascade="all, delete-orphan")
    profile = relationship("Profile",back_populates="user")
    
    groups = relationship("Group", secondary=user_group, backref="users")
    
    def __repr__(self):
        return f"id:{self.id}, name:{self.name}, age:{self.name}, email:{self.email}"

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer , primary_key=True)
    title = Column(String , nullable=False)
    content = Column(String , nullable=False)
    user_id = Column(Integer , ForeignKey("users.id"))
    
    user = relationship("User" , back_populates="posts")
    comments = relationship("Comment",back_populates="post",cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"id:{self.id}, title:{self.title}, content:{self.content}, user_id:{self.user_id}"
    
class Comment(Base): 
    __tablename__ = "comments"
    
    id = Column(Integer , primary_key=True)
    content = Column(String , nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    
class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer , primary_key=True)
    date_of_birth = Column(Date, nullable=False)
    profile_picture = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    user_id = Column(Integer,ForeignKey("users.id"),unique=True)
    
    user =  relationship("User",back_populates="profile")
    
    def __repr__(self):
        return f"id:{self.id}, date_of_birth:{self.date_of_birth}, profile_picture:{self.profile_picture}, bio:{self.bio}, user_id:{self.user_id}"
    


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer , primary_key=True)
    name = Column(String , nullable=False)
    description = Column(String , nullable=True)
    
    users = relationship("User", secondary=user_group, backref="groups")
    
    def __repr__(self):
        return f"id:{self.id}, name:{self.name}, description:{self.description}"
        
        
          
    
Base.metadata.create_all(engine)    