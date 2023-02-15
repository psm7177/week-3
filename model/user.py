from typing import Optional
from sqlmodel import SQLModel, Field

from pydantic import BaseModel

class UserViewModel(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, index=True,primary_key=True)
    username: str = Field(index=True)
    password: str