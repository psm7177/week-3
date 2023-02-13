from typing import Union
from fastapi import APIRouter
from pydantic import BaseModel

from model.todo import TodoListViewModel, TodoViewModel
from service.todo_service import TodoService

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
    responses={404: {"description": "Not found"}},
)

class CreateTodoParm(BaseModel):
    title: str

@router.post('/')
async def create_todo(param: CreateTodoParm):
    return await TodoService.create_todo(param.title)

@router.get('/')
async def read_todo_list():
    return await TodoService.read_todo_list()

@router.get('/{todo_id}')
async def read_todo(todo_id: int):
    return  await TodoService.read_todo(todo_id)

    
class UpdateTodoParm(BaseModel):
    title: Union[str, None] = None
    primary: Union[bool, None] = None

@router.put('/{todo_id}')
async def update_todo(todo_id: int, param: UpdateTodoParm):
    return await TodoService.update_todo(todo_id, param.title, param.primary)

@router.delete('/{todo_id}')
async def update_todo(todo_id: int):
    return await TodoService.delete_todo(todo_id)