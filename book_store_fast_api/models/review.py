from ..core.database import *
from .book import Book

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer , primary_key=True)
    content = Column(Text, nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"),nullable=False)
    
    book = relationship("Book",back_populates="reviews")