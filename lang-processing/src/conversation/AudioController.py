from fastapi import APIRouter, HTTPException, status

from typing import List

from models.user.user import User
from models.user.user_in import UserIn
from models.user.user_out import UserOut


router = APIRouter()

@router.get("/audios/", response_model=List[UserOut], tags=["audio"])
def list_account():
    """Lists all Messages"""
    return DB.getUsers()

@router.post("/audios/", response_model=UserOut, status_code=status.HTTP_201_CREATED, tags=["audio"])
def create_account(userIn: UserIn):
    """Creates a New Account"""
    user_dict = userIn.model_dump()

    user_dict['id_user'] = DB.usersNextID
    DB.usersIncID() 
    user_dict['senha'] = str(hash(user_dict['senha'] + user_dict['nome']))
    user = User(**user_dict)
    DB.users[user.id_user] = user

    return DB.getUser(user.id_user)
