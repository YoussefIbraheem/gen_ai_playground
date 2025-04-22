from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .core.database import Base , engine
from .routes import router as book_router
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(book_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",reload=True)