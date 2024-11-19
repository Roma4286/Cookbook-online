from typing import Optional, List

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import BaseModel

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)
    recipes = Column(JSONB, nullable=True, index=True)

class Ingredients(BaseModel):
    name: str
    quantity: str
    note: Optional[str]

class Recipes(BaseModel):
    name_dish: str
    ingredients: List[Ingredients]
    description: str