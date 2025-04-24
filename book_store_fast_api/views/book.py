from fastapi import Request, APIRouter, Depends, Query, Form
from fastapi.responses import RedirectResponse
from ..core.database import get_db
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from ..models.book import Book, Author

router = APIRouter(prefix="/books")

templates = Jinja2Templates(directory="templates")


@router.get("/", include_in_schema=False)
def web_list_books(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book)
    return templates.TemplateResponse(
        "list_books.html", {"request": request, "books": books}
    )


@router.get("/create", include_in_schema=False)
def get_create_form(request: Request, db: Session = Depends(get_db)):
    authors = db.query(Author)
    return templates.TemplateResponse(
        "create_book.html", {"authors": authors, "request": request}
    )


@router.post("/create", include_in_schema=False)
async def web_create_book(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    author_id: str = Form(...),
    db: Session = Depends(get_db),
):
    created_book = Book(title=title, description=description, author_id=author_id)
    db.add(created_book)
    db.commit()
    db.refresh(created_book)
    return RedirectResponse(
        request.url_for("web_list_books"), status_code=303
    )

@router.get("/update/{id}", include_in_schema=False)
def get_update_form(request: Request, id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter_by(id=id).first()
    if not book:
        return templates.TemplateResponse(
            "404.html", {"request": request, "message": "Book not found!"}
        )
    authors = db.query(Author)
    return templates.TemplateResponse(
        "update_book.html",
        {"book": book, "authors": authors, "request": request},
    )
    
@router.post("/update/{id}", include_in_schema=False)
async def web_update_book(
    request: Request,
    id: int,
    title: str = Form(...),
    description: str = Form(...),
    author_id: str = Form(...),
    db: Session = Depends(get_db),
):
    book = db.query(Book).filter_by(id=id).first()
    if not book:
        return templates.TemplateResponse(
            "404.html", {"request": request, "message": "Book not found!"}
        )
    book.title = title
    book.description = description
    book.author_id = author_id
    db.commit()
    db.refresh(book)
    return RedirectResponse(
        request.url_for("web_list_books"), status_code=303
    )   


@router.post('/delete/{id}', include_in_schema=False)
def web_delete_book(
    request: Request,
    id: int,
    db: Session = Depends(get_db)):
    
    book = db.query(Book).filter_by(id=id).first()
    if not book:
        return templates.TemplateResponse(
            "404.html", {"request": request, "message": "Book not found!"}
        )
    db.delete(book)
    db.commit()
    return RedirectResponse(
        request.url_for("web_list_books"), status_code=303
    )     
    
    