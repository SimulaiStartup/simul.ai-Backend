from sqlalchemy.orm import Session
from fastapi import HTTPException

from .Roteiro import Roteiro
from .RoteiroDTO import RoteiroIn
from ..roteiroStage.RoteiroStageRepository import RoteiroStageRepository
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
    
    #def get_by_conversation(db: Session, id_conversation: int) -> List[Roteiro]:
        roteiros = db.query(Roteiro).filter(Roteiro.id_conversation == id_conversation).all()
        if len(roteiros) == 0:
            raise HTTPException(status_code=404, detail="Nenhuma conversa encontrada para o ID enviado")  
        return roteiros

    def create(db: Session, roteiro: RoteiroIn) -> Roteiro:
        roteiro = Roteiro(**roteiro.model_dump())
        db.add(roteiro)
        db.commit()
        db.refresh(roteiro)
        return roteiro

    def delete(db: Session, id_roteiro: int):
        RoteiroStageRepository.delete_all_by_roteiro(db, id_roteiro)
        rows_deleted = db.query(Roteiro).filter(Roteiro.id_roteiro == id_roteiro).delete()
        db.commit()
        if rows_deleted == 0:
            raise HTTPException(status_code=404, detail="Roteiro não encontrada")