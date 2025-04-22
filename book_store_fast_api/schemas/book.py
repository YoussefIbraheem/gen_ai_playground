from pydantic import BaseModel
from typing import Optional , List


class BooksListResponseSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    author_id: int


class createBookRequestSchema(BaseModel):
    title: str
    description: Optional[str]
    author_id: int
