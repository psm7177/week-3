from typing import Optional,List
from sqlmodel import Field, SQLModel

from pydantic import BaseModel

class TodoViewModel(BaseModel):
    id: int
    title: str
    primary: bool

    class Config:
        orm_mode = True

class TodoListViewModel(BaseModel):
    todos: List[TodoViewModel]

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    primary: bool