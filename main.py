# main.py
from fastapi import FastAPI

from controller import todo, user

from infra.database import create_db_and_tables
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(todo.router)
app.include_router(user.router)