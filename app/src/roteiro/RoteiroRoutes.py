from fastapi import APIRouter, HTTPException, status # type: ignore

from typing import List
from .RoteiroDTO import RoteiroIn, RoteiroOut
from .Roteiro import Roteiro
from .RoteiroRepository import RoteiroRepository
from database import get_db

router = APIRouter()
db = get_db()

@router.get("/roteiros/{id_roteiro}", response_model=RoteiroOut, tags=["roteiro"])
def get_roteiro(id_roteiro: int = None): 
    """Returns a Specific Roteiro based on the id"""
    return RoteiroRepository.get(db,id_roteiro).to_roteiroOut()

@router.get("/roteiros", response_model=List[RoteiroOut], tags=["roteiro"])
def get_all(): 
    """Returns a Specific Roteiro based on the id"""
    return list(map(lambda x: x.to_roteiroOut(), RoteiroRepository.get_all(db)))

@router.post("/roteiros", response_model=RoteiroOut, status_code=status.HTTP_201_CREATED, tags=["roteiro"])
def new_roteiro(movIn : RoteiroIn):
    """Creates a New Roteiro"""
    return RoteiroRepository.create(db,movIn).to_roteiroOut()

@router.delete("/roteiros/{id_roteiro}", status_code=status.HTTP_204_NO_CONTENT, tags=["roteiro"])
def deleta_roteiro(id_roteiro: int):
    """Deletes a Roteiro's information"""
    return RoteiroRepository.delete(db,id_roteiro)
