from pydantic import BaseModel
from typing import Optional , List

class ReviewResponseSchema(BaseModel):
    id: int
    content: str
    book_id: int