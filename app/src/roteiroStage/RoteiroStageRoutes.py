from fastapi import APIRouter, HTTPException, status # type: ignore

from typing import List
from .RoteiroStageDTO import RoteiroStageIn, RoteiroStageOut
from .RoteiroStage import RoteiroStage
from .RoteiroStageRepository import RoteiroStageRepository
from database import get_db

router = APIRouter()
db = get_db()

@router.get("/roteiros/stages/{id_roteiro}", response_model=List[RoteiroStage], tags=["roteiro"])
def get_roteiro(id_roteiro: int = None): 
    """Returns a Specific RoteiroStage based on the id"""
    if id_roteiro:
        return [RoteiroStageRepository.get(db,id_roteiro)]
    else:
        return RoteiroStageRepository.get_all(db)
    
@router.get("/roteiros/stages/roteiro/{id_roteiro}", response_model=List[RoteiroStage], tags=["roteiro"])
def get_roteiro(id_roteiro: int): 
    """Returns all options based on the id for the Roteiro"""
    return RoteiroStageRepository.get_all_by_roteiro(db,id_roteiro)

@router.get("/roteiros/stages/roteiro/{id_roteiro}/{id_stage}", response_model=List[RoteiroStage], tags=["roteiro"])
def get_roteiro(id_roteiro: int, id_stage: int): 
    """Returns all options based on the id for the roteiro and the stage"""
    return RoteiroStageRepository.get_by_stage_and_roteiro(id_stage, id_roteiro)
    
@router.post("/roteiros/stages", response_model=RoteiroStageOut, status_code=status.HTTP_201_CREATED, tags=["roteiro"])
def new_roteiro(movIn : RoteiroStageIn):
    """Creates a New RoteiroStage"""
    return RoteiroStageRepository.create(db,movIn)

@router.delete("/roteiros/stages/{id_roteiro}", status_code=status.HTTP_204_NO_CONTENT, tags=["roteiro"])
def deleta_roteiro(id_roteiro: int):
    """Deletes a Roteiros information"""
    return RoteiroStageRepository.delete_all_by_roteiro(db,id_roteiro)

@router.delete("/roteiros/stages/stage/{id_roteiroStage}", status_code=status.HTTP_204_NO_CONTENT, tags=["roteiro"])
def deleta_roteiro(id_roteiroStage: int):
    """Deletes a Roteiros information"""
    return RoteiroStageRepository.delete(db,id_roteiroStage)

@router.delete("/roteiros/stages/conversation/{id_conversation}", status_code=status.HTTP_204_NO_CONTENT, tags=["roteiro"])
def deleta_roteiro(id_conversation: int):
    """Deletes an entire Conversation's information"""
    return RoteiroStageRepository.delete_conversation(db,id_conversation)