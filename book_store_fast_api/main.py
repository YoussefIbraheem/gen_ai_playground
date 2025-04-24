from fastapi import FastAPI
from .core.database import Base , engine
from .routes.book import router as book_router
from .routes.author import router as author_router
from .views.book import router as book_web_routes
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(book_router)
app.include_router(author_router)
app.include_router(book_web_routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",reload=True)