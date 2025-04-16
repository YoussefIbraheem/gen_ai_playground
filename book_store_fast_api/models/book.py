from core.database import *

class Book(Base):
    __tablename__= "books"
    
    id = Column(Integer , primary_key=True)
    title = Column(String , nullable=False)
    author_id = Column(Integer , ForeignKey('author.id'))
    
    author = relationship("Author",back_populates="books")
    reviews = relationship("Review",back_populates="book")
    

