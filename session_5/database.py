from sqlalchemy import create_engine , String , Integer , Column , ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 


engine = create_engine('sqlite:///crud_op.db', echo=True)

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    
    def __repr__(self):
        return f"<Task(title='{self.title}', description='{self.description}')>"
    


Base.metadata.create_all(bind = engine)

Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def create_task(title, description):
    session = get_session()
    new_task = Task(title=title, description=description)
    session.add(new_task)
    session.commit()
    session.close()
    
def get_tasks():
    session = get_session()
    tasks = session.query(Task).all()
    session.close()
    return tasks

def update_task(task_id, title, description):
    session = get_session()
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        task.title = title
        task.description = description
        session.commit()
    session.close()    
    
def delete_task(task_id):
    session = get_session()
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        session.delete(task)
        session.commit()
    session.close()    