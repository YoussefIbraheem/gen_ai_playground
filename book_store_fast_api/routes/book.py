from fastapi import APIRouter , Depends , Query
from ..models import Book
from ..schemas.book import BooksListResponseSchema , List , createBookRequestSchema
from sqlalchemy.orm import Session
from ..core.database import get_db

router = APIRouter(prefix='/apis/books')


@router.get('/', response_model=List[BooksListResponseSchema])
def list_books(db:Session=Depends(get_db)):
    books = db.query(Book)
    return books
    
@router.post('/',response_model=BooksListResponseSchema)
def create_book(request_params:createBookRequestSchema,db:Session=Depends(get_db)):
    db_book = Book(**request_params.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book   