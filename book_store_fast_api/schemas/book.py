from pydantic import BaseModel
from typing import Optional , List


class BookResponseSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    author_id: int
   


class CreateBookRequestSchema(BaseModel):
    title: str
    description: Optional[str]
    author_id: int
    

class UpdateBookRequestSchema(BaseModel):   
    title: str
    description: Optional[str]
    author_id: int 
