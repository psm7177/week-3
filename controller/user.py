from fastapi import APIRouter
from pydantic import BaseModel

from service.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=['user'],
    responses={404: {"description": "Not found"}},
)

class RegisterUserParams(BaseModel):
    username: str
    password: str

@router.post('/register')
async def register_user(params: RegisterUserParams):
    return await UserService.register_user(params.username, params.password)

class LoginParams(BaseModel):
    username: str
    password: str

@router.post('/login')
async def login(params: LoginParams):
    return await UserService.login(params.username, params.password)