from infra.exception import EngineNoneTypeException
import secret

from model import *
from sqlmodel import  SQLModel, create_engine, Session,select
from sqlalchemy.future import Engine

print(secret.mysql_connection_string)

engine = create_engine(secret.mysql_connection_string,echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db_engine()-> Engine:
    if engine == None:
        raise EngineNoneTypeException("The engine is None")
    return engine

def get_db_session():
    return Session(get_db_engine())

def get_by_id(table, id):
    with get_db_session() as session:
        statement = select(table).where(table.id ==id)
        return session.exec(statement).one_or_none()