from typing import Union

from fastapi import HTTPException, status
from sqlmodel import select

from infra.database import get_db_session
from model.todo import Todo, TodoListViewModel, TodoViewModel

class TodoService:
    async def create_todo(title:str):
        todo = Todo(title=title, primary=False)
        with get_db_session() as session:
            session.add(todo)
            session.commit()

            return TodoViewModel.from_orm(todo)

    async def read_todo_list():
        with get_db_session() as session:
            stat = select(Todo)
            results = session.exec(stat)

            todos = [TodoViewModel.from_orm(r) for r in results]
            return TodoListViewModel(todos = todos)

    async def read_todo(id: int):
        with get_db_session() as session:
            stat = select(Todo).where(Todo.id == id)
            results = session.exec(stat)
            todo = results.one_or_none()

            if todo is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="InvalidationRequest: This todo_id does not exist")
            return TodoViewModel.from_orm(todo)
    
    async def update_todo(id: int, title: Union[str, None], primary: Union[bool, None]):
        with get_db_session() as session:
            stat = select(Todo).where(Todo.id == id)
            results = session.exec(stat)
            todo = results.one_or_none()

            if todo is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="InvalidationRequest: This todo_id does not exist")
            
            if title is not None:
                todo.title = title
            
            if primary is not None:
                todo.primary = primary
            
            session.add(todo)
            session.commit()
            session.refresh(todo)

            return TodoViewModel.from_orm(todo)
    
    async def delete_todo(id: int):
        with get_db_session() as session:
            stat = select(Todo).where(Todo.id == id)
            results = session.exec(stat)
            todo = results.one_or_none()

            if todo is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="InvalidationRequest: This todo_id does not exist")
            
            session.delete(todo)
            session.commit()

            return TodoViewModel.from_orm(todo)

