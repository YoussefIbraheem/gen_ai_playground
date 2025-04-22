from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .core.database import Base , engine
from .routes.book import router as book_router
from .routes.author import router as author_router
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(book_router)
app.include_router(author_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",reload=True)