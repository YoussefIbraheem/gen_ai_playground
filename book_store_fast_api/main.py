from fastapi import FastAPI , Request
from fastapi.responses import RedirectResponse
from .core.database import Base , engine
from .routes.book import router as book_router
from .routes.author import router as author_router
from .views.book import router as book_web_routes
from fastapi.templating import Jinja2Templates
app = FastAPI()

Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")
app.include_router(book_router)
app.include_router(author_router)
app.include_router(book_web_routes)
@app.route('/')
def home_page(request:Request):
   return RedirectResponse(
        request.url_for("web_list_books"), status_code=303
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",reload=True)