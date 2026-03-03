from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from pydantic import BaseModel

# Database Models
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str

class RegexFavorite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    pattern: str
    explanation: str
    title: str

class PaletteFavorite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    colors: str # JSON string of hex codes

class QuoteFavorite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    text_en: str
    text_es: str
    author: str

class DataFavorite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    data_type: str
    content: str # JSON string of generated data

# Request/Response Models
class FormatRequest(BaseModel):
    code: str
    language: str

class RegexRequest(BaseModel):
    regex: str
    text: Optional[str] = None

class DataGenRequest(BaseModel):
    type: str
    count: int = 10
