from fastapi import APIRouter, HTTPException, status # type: ignore

from typing import List
from .RoteiroDTO import RoteiroIn, RoteiroOut
from .Roteiro import Roteiro
from .RoteiroRepository import RoteiroRepository
from database import get_db

router = APIRouter()
db = get_db()

@router.get("/roteiros/{id_roteiro}", response_model=List[Roteiro], tags=["roteiro"])
def get_roteiro(id_roteiro: int = None): 
    """Returns a Specific Roteiro based on the id"""
    if id_roteiro:
        return [RoteiroRepository.get(db,id_roteiro)]
    else:
        return RoteiroRepository.get_all(db)

@router.post("/roteiros", response_model=RoteiroOut, status_code=status.HTTP_201_CREATED, tags=["roteiro"])
def new_roteiro(movIn : RoteiroIn):
    """Creates a New Roteiro"""
    return RoteiroRepository.create(db,movIn)

@router.delete("/roteiros/{id_roteiro}", status_code=status.HTTP_204_NO_CONTENT, tags=["roteiro"])
def deleta_roteiro(id_roteiro: int):
    """Deletes a Roteiro's information"""
    return RoteiroRepository.delete(db,id_roteiro)

@router.delete("/roteiros/conversation/{id_conversation}", status_code=status.HTTP_204_NO_CONTENT, tags=["roteiro"])
def deleta_roteiro(id_conversation: int):
    """Deletes an entire Conversation's information"""
    return RoteiroRepository.delete_conversation(db,id_conversation)