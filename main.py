# main.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Union

app = FastAPI()

counter = 0
todos = {}

class Todo(BaseModel):
    id: int
    title: str
    primary: bool

class CreateTodoParm(BaseModel):
    title: str

@app.post('/todo')
async def create_todo(param: CreateTodoParm):
    global counter

    todo = Todo(id=counter, title=param.title, primary=False)

    counter += 1

    todos[todo.id] = todo

    return todo

class TodoList(BaseModel):
    todos: List[Todo]

@app.get('/todo-list')
async def read_todo_list():
    return TodoList(todos=list(todos.values()))

@app.get('/todo/{todo_id}')
async def read_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="InvalidationRequest: This todo_id does not exist")

    return todos[todo_id]

class UpdateTodoParm(BaseModel):
    title: Union[str, None] = None
    primary: Union[bool, None] = None

@app.patch('/todo/{todo_id}')
async def update_todo(todo_id: int, param: UpdateTodoParm):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="InvalidationRequest: This todo_id does not exist")
    
    todo = todos[todo_id]

    if param.title is not None:
        todo.title = param.title

    if param.primary is not None:
        todo.primary = param.primary

    return todo

@app.delete('/todo/{todo_id}')
async def update_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="InvalidationRequest: This todo_id does not exist")
    
    todo = todos.pop(todo_id)

    return todo

@app.delete('/todo-list')
async def delete_todo_list():
    todos.clear()
    return {'success': True}
