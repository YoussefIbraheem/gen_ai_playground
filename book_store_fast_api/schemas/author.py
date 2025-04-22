from pydantic import BaseModel
from typing import Optional , List


class AuthorResponseSchema(BaseModel):
    id:int
    name:str
    age: Optional[int]
    

class AuthorRequestSchema(BaseModel):
    name:str
    age: Optional[int]    
    
    