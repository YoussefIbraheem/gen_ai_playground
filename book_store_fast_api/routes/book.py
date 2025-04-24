from .common_dependencies import *
from ..models.book import Book
from ..schemas.book import (
    CreateBookRequestSchema,
    BookResponseSchema,
    UpdateBookRequestSchema,
    List,
    Optional
)

router = APIRouter(prefix="/apis/books")


@router.get("/", response_model=List[BookResponseSchema])
def list_books(
     search: Optional[str] = Query(None,description="Search by name or description"),
    order_by: Optional[str]= Query(None,description="Order by id or title"),
    db: Session = Depends(get_db)):
    books = db.query(Book)
    if search:
        print(search)
        books = books.filter((Book.title.ilike(f'%{search}%')) | (Book.description.ilike(f'%{search}%')))
    if order_by:
        if order_by.lower() == "id":
            books = books.order_by(Book.id)
        elif order_by.lower() == "title":
            books = books.order_by(Book.title)
    return books.all()


@router.get("/{id}", response_model=BookResponseSchema)
def get_book(id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter_by(id=id).first()
    if not book:
        raise HTTPException(status_code=404,detail="NOT FOUND",headers={'error':"Book not found!"})
        
    return book


@router.post("/", response_model=BookResponseSchema)
def create_book(request_params: CreateBookRequestSchema, db: Session = Depends(get_db)):
    db_book = Book(**request_params.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.put("/{id}", response_model=BookResponseSchema)
def update_book(request_params: UpdateBookRequestSchema,id,db: Session = Depends(get_db)):
    book = db.query(Book).filter_by(id=id).first()
    params = request_params.model_dump()
    for param_key , param_value in params.items():
        setattr(book,param_key,param_value)
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{id}")
def delete_book(id, db: Session = Depends(get_db)):
    book = db.query(Book).filter_by(id=id).first()
    if not book:
        raise HTTPException(status_code=404,detail="NOT FOUND",headers={'error':"Book not found!"})
    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"} 
    
