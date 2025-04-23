from .book import *
from .author import *
from fastapi import APIRouter, Depends, Query
from ..models import Author
from ..schemas.author import AuthorRequestSchema, List, AuthorResponseSchema
from sqlalchemy.orm import Session
from ..core.database import get_db