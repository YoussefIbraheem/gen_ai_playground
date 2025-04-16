from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.database import Base , engine
app = FastAPI()

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",reload=True)