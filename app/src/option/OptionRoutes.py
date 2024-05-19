from fastapi import APIRouter, HTTPException, status # type: ignore

from typing import List
from .OptionDTO import OptionIn, OptionOut
from .Option import Option
from .OptionRepository import OptionRepository
from database import get_db

router = APIRouter()
db = get_db()


@router.get("/options/roteiro/{id_roteiro}", response_model=List[OptionOut], tags=["option"])
def get_all_options_by_roteiro(id_roteiro: int): 
    """Returns all options based on the id for the Roteiro"""
    return list(map(lambda x: x.to_optionOut(), OptionRepository.get_all_by_roteiro(db,id_roteiro)))

@router.get("/options/{id_option}", response_model=OptionOut, tags=["option"])
def get_roteiro_option(id_option: int):
    """Returns a Specific Option based on the id"""
    return OptionRepository.get(db,id_option).to_optionOut()

@router.get("/options/roteiro/{id_roteiro}/tag/{tag}", response_model=List[OptionOut], tags=["option"])
def get_by_tag_and_roteiro(id_roteiro: int, tag: str): 
    """Returns all options based on the id for the roteiro and the tag"""
    return list(map(lambda x: x.to_optionOut(), OptionRepository.get_by_tag_and_roteiro(db,tag,id_roteiro)))
    
@router.post("/options/", response_model=OptionOut, status_code=status.HTTP_201_CREATED, tags=["option"])
def new_roteiro_option(movIn : OptionIn):
    """Creates a New Option"""
    return OptionRepository.create(db,movIn).to_optionOut()

@router.delete("/options/{id_roteiro}", status_code=status.HTTP_204_NO_CONTENT, tags=["option"])
def delete_all_by_roteiro(id_roteiro: int):
    """Deletes a Roteiros information"""
    return OptionRepository.delete_all_by_roteiro(db,id_roteiro)

@router.delete("/options/{id_option}/option", status_code=status.HTTP_204_NO_CONTENT, tags=["option"])
def delete_roteiro_option(id_option: int):
    """Deletes a Roteiros information"""
    return OptionRepository.delete(db,id_option)
