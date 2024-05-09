from fastapi import APIRouter, HTTPException, status # type: ignore

from typing import List
from .RoteiroStageDTO import RoteiroStageIn, RoteiroStageOut
from .RoteiroStage import RoteiroStage
from .RoteiroStageRepository import RoteiroStageRepository
from database import get_db

router = APIRouter()
db = get_db()

# Não entendi o ponto dessas rotas
#@router.get("/roteiros/stages/", response_model=List[RoteiroStageOut], tags=["roteiro"])
#def get_all(): 
"""Returns a Specific RoteiroStage based on the id"""
    #return list(map(lambda x: x.to_roteiroStageOut(), RoteiroStageRepository.get_all(db)))
    
#@router.get("/roteiros/stages/{id_roteiro}", response_model=List[RoteiroStageOut], tags=["roteiro"])
#def get_roteiro(id_roteiro: int = None): 
"""Returns a Specific RoteiroStage based on the id"""
    #return [RoteiroStageRepository.get(db,id_roteiro).to_roteiroStageOut()]
 
    
@router.get("/stages/{id_roteiro}", response_model=List[RoteiroStageOut], tags=["roteiro"])
def get_all_stages_by_roteiro(id_roteiro: int): 
    """Returns all options based on the id for the Roteiro"""
    return list(map(lambda x: x.to_roteiroStageOut(), RoteiroStageRepository.get_all_by_roteiro(db,id_roteiro)))

@router.get("/stages/{id_roteiroStage}/stage", response_model=RoteiroStageOut, tags=["roteiro"])
def get_roteiro_stage(id_roteiroStage: int):
    """Returns a Specific RoteiroStage based on the id"""
    return RoteiroStageRepository.get(db,id_roteiroStage).to_roteiroStageOut()

@router.get("/stages/{id_roteiro}/{stage}", response_model=List[RoteiroStageOut], tags=["roteiro"])
def get_by_stage_and_roteiro(id_roteiro: int, stage: int): 
    """Returns all options based on the id for the roteiro and the stage"""
    return list(map(lambda x: x.to_roteiroStageOut(), RoteiroStageRepository.get_by_stage_and_roteiro(db,stage,id_roteiro)))
    
@router.post("/stages/", response_model=RoteiroStageOut, status_code=status.HTTP_201_CREATED, tags=["roteiro"])
def new_roteiro_stage(movIn : RoteiroStageIn):
    """Creates a New RoteiroStage"""
    return RoteiroStageRepository.create(db,movIn).to_roteiroStageOut()

@router.delete("/stages/{id_roteiro}", status_code=status.HTTP_204_NO_CONTENT, tags=["roteiro"])
def delete_all_by_roteiro(id_roteiro: int):
    """Deletes a Roteiros information"""
    return RoteiroStageRepository.delete_all_by_roteiro(db,id_roteiro)

@router.delete("/stages/{id_roteiroStage}/stage", status_code=status.HTTP_204_NO_CONTENT, tags=["roteiro"])
def delete_roteiro_stage(id_roteiroStage: int):
    """Deletes a Roteiros information"""
    return RoteiroStageRepository.delete(db,id_roteiroStage)
