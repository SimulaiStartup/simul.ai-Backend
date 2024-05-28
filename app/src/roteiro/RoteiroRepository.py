from sqlalchemy.orm import Session
from fastapi import HTTPException

from .Roteiro import Roteiro
from .RoteiroDTO import RoteiroIn
from ..option.OptionRepository import OptionRepository
from typing import List

class RoteiroRepository:
    def get(db: Session, id_roteiro: int) -> Roteiro:
        roteiro = db.query(Roteiro).filter(Roteiro.id_roteiro == id_roteiro).first()
        if roteiro:
            return roteiro
        raise HTTPException(status_code=404, detail="Roteiro não encontrado")

    def get_all(db: Session) -> List[Roteiro]:
        roteiros = db.query(Roteiro).all()
        return roteiros

    def create(db: Session, roteiro: RoteiroIn) -> Roteiro:
        roteiro = Roteiro(**roteiro.model_dump())
        db.add(roteiro)
        db.commit()
        db.refresh(roteiro)
        return roteiro

    def delete(db: Session, id_roteiro: int):
        OptionRepository.delete_all_by_roteiro(db, id_roteiro)
        rows_deleted = db.query(Roteiro).filter(Roteiro.id_roteiro == id_roteiro).delete()
        db.commit()
        if rows_deleted == 0:
            raise HTTPException(status_code=404, detail="Roteiro não encontrada")