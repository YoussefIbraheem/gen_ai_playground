from .common_dependencies import *
from ..models.book import Book
from ..schemas.book import CreateBookRequestSchema , BookResponseSchema , List
router = APIRouter(prefix="/apis/books")


@router.get("/", response_model=List[BookResponseSchema])
def list_books(db: Session = Depends(get_db)):
    books = db.query(Book)
    return books


@router.get("/{id}", response_model=BookResponseSchema)
def get_book(id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter_by(id=id).first()
    return book


@router.post("/", response_model=BookResponseSchema)
def create_book(request_params: CreateBookRequestSchema, db: Session = Depends(get_db)):
    db_book = Book(**request_params.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
