from sqlalchemy.orm import Session
from fastapi import HTTPException

from .RoteiroStage import RoteiroStage
from .RoteiroStageDTO import RoteiroStageIn
from typing import List

class RoteiroStageRepository:
    def get(db: Session, id_roteiroStage: int) -> RoteiroStage:
        roteiro = db.query(RoteiroStage).filter(RoteiroStage.id_roteiroStage == id_roteiroStage).first()
        if roteiro:
            return roteiro
        raise HTTPException(status_code=404, detail="Roteiro não Encontrado")

    def get_all(db: Session) -> List[RoteiroStage]:
        options = db.query(RoteiroStage).all()
        return options
    
    def get_all_by_roteiro(db: Session, id_roteiro:int) -> List[RoteiroStage]:
        options = db.query(RoteiroStage).filter(RoteiroStage.id_roteiro == id_roteiro).all()
        if len(options) == 0:
            raise HTTPException(status_code=404, detail="Nenhum roteiro encontrado para o ID enviado")  
        return options
    
    def get_by_stage_and_roteiro(db: Session, stage: int, id_roteiro: int) -> List[RoteiroStage]:
        options = db.query(RoteiroStage).filter(RoteiroStage.stage == stage, RoteiroStage.id_roteiro == id_roteiro).all()
        if len(options) == 0:
            raise HTTPException(status_code=404, detail="Nenhuma opção encontrada para os IDs enviados")  
        return options

    def create(db: Session, roteiro: RoteiroStageIn) -> RoteiroStage:
        roteiro = RoteiroStage(**roteiro.model_dump())
        db.add(roteiro)
        db.commit()
        db.refresh(roteiro)
        return roteiro

    def delete(db: Session, id_roteiroStage: int):
        rows_deleted = db.query(RoteiroStage).filter(RoteiroStage.id_roteiroStage == id_roteiroStage).delete()
        db.commit()
        if rows_deleted == 0:
            raise HTTPException(status_code=404, detail="Opção não encontrada")

    def delete_all_by_roteiro(db: Session, id_roteiro: int):
        rows_deleted = db.query(RoteiroStage).filter(RoteiroStage.id_roteiro == id_roteiro).delete()
        db.commit()
        if rows_deleted == 0:
            raise HTTPException(status_code=404, detail="Roteiro não encontrado")