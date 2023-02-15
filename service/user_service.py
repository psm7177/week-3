from fastapi import HTTPException, status
from sqlmodel import select
from infra.database import get_db_session

from model.user import User, UserViewModel
from infra.crypto import pwd_context

class UserService:
    async def register_user(username:str, password: str):
        with get_db_session() as session:
            statement = select(User).where(User.username== username)
            result = session.exec(statement)
            user = result.one_or_none()
            
            if user is not None:
                raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT, detail="InvalidationRequest: This user already exist.")
            
            new_user = User(username=username, password=pwd_context.hash(password))
            session.add(new_user)
            session.commit()

            return UserViewModel.from_orm(new_user)
    
    async def login(username: str, password:str):
        with get_db_session() as session:
            statement = select(User).where(User.username ==username)
            result = session.exec(statement)
            user = result.one_or_none()

            if user is None :
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="InvalidationRequest: This user does not exist.")

            if not pwd_context.verify(password,user.password): 
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="BadRequest: The password is not for this user.")

            return UserViewModel.from_orm(user)