from fastapi import APIRouter, HTTPException, status

from typing import List
from .ChecklistDTO import ChecklistIn, ChecklistOut, ChecklistCreate
from .Checklist import Checklist
from .ChecklistRepository import ChecklistRepository
from database import get_db

router = APIRouter()
db = get_db()

@router.get("/checklists/roteiro/{id_roteiro}", response_model=List[ChecklistOut], tags=["checklist"])
def get_all_checklists_by_roteiro(id_roteiro: int):
    """Returns all checklist questions for a roteiro"""
    return list(map(lambda x: x.to_checklistOut(), ChecklistRepository.get_all_checklists_by_roteiro(db,id_roteiro)))

@router.get("/checklists/{id_checklist}", response_model=ChecklistOut, tags=["checklist"])
def get_roteiro_checklist(id_checklist: int):
    """Returns a checklist based on checklist_id"""
    return ChecklistRepository.get(db,id_checklist).to_checklistOut()


@router.post("/checklists/", response_model=ChecklistOut, status_code=status.HTTP_201_CREATED, tags=["checklist"])
def create_checklist(checklist: ChecklistCreate):
    """Creates a new checklist"""
    return ChecklistRepository.create(db,checklist).to_checklistOut()

@router.post("/checklists/list", response_model=List[ChecklistOut], status_code=status.HTTP_201_CREATED, tags=["checklist"])
def create_checklist_by_list(list_checklist = List[ChecklistIn]):
    saida = []
    for checklist in list_checklist:
        saida.append(ChecklistRepository.create(db,checklist).to_optionOut())
    return saida

@router.delete("/checklists/{id_checklist}", status_code=status.HTTP_204_NO_CONTENT, tags=["checklist"])
def delete_checklist(id_checklist: int):
    """Deletes a checklist"""
    return ChecklistRepository.delete(db,id_checklist)

@router.delete("/checklists/roteiro/{id_roteiro}", status_code=status.HTTP_204_NO_CONTENT, tags=["checklist"])
def delete_all_checklists_by_roteiro(id_roteiro: int):
    """Deletes all checklists from a roteiro"""
    return ChecklistRepository.delete_all_by_roteiro(db,id_roteiro)
    