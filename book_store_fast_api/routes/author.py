from fastapi import APIRouter, Depends, Query
from ..models import Author
from ..schemas.author import AuthorRequestSchema, List, AuthorResponseSchema
from sqlalchemy.orm import Session
from ..core.database import get_db

router = APIRouter(prefix="/apis/authors")


@router.get("/", response_model=List[AuthorResponseSchema])
def list_authors(db: Session = Depends(get_db)):
    authors_list = db.query(Author)
    return authors_list


@router.get("/{id}")
def get_author(id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter_by(id=id).first()
    return author


@router.post("/", response_model=AuthorResponseSchema)
def create_author(request_params: AuthorRequestSchema, db: Session = Depends(get_db)):
    db_author = Author(**request_params.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
