from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .ChecklistDTO import ChecklistIn
from .Checklist import Checklist


class ChecklistRepository:
    def get_all_checklists_by_roteiro(db:Session, id_roteiro:int) -> List[Checklist]:
        checklists = db.query(Checklist).filter(Checklist.id_roteiro == id_roteiro).all()
        if len(checklists) == 0:
            raise HTTPException(status_code=404, detail="Nenhuma checklist encontrada ou roteiro inexistente")
        return checklists
    
    def get(db:Session, id_checklist:int) -> Checklist:
        checklist = db.query(Checklist).filter(Checklist.id_checklist == id_checklist).first()
        if checklist:
            return checklist
        raise HTTPException(status_code=404, detail="Checklist não encontrada")
    
    def create(db:Session, checklist:ChecklistIn) -> Checklist:
        try:
            checklist = Checklist(**checklist.model_dump())
            db.add(checklist)
            db.commit()
            db.refresh(checklist)
            return checklist
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Erro ao criar checklist: {e}")

    def delete(db:Session, id_checklist:int):
        rows_deleted = db.query(Checklist).filter(Checklist.id_checklist == id_checklist).delete()
        db.commit()
        if rows_deleted == 0:
            raise HTTPException(status_code=404, detail="Checklist não encontrada")