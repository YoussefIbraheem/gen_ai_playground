from ..core.database import *
from .author import Author


class Book(Base):
    __tablename__= "books"
    
    id = Column(Integer , primary_key=True)
    title = Column(String , nullable=False)
    description = Column(Text, nullable=True)
    author_id = Column(Integer , ForeignKey("authors.id"), nullable=False)
    
    author = relationship("Author",back_populates="books")
   
    reviews = relationship("Review",back_populates="book")

