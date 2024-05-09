from sqlalchemy.orm import Session
from fastapi import HTTPException

from .RoteiroStage import RoteiroStage
from .RoteiroStageDTO import RoteiroStageIn
from typing import List

class RoteiroStageRepository:
    #def get(db: Session, id_roteiroStage: int) -> RoteiroStage:
        #roteiro_stages = db.query(RoteiroStage).filter(RoteiroStage.id_roteiroStage == id_roteiroStage).all()
        #if roteiro_stages:
            #return roteiro_stages
        #raise HTTPException(status_code=404, detail="Roteiro Inexistente ou Nenhum Estágio Encontrado")
    
    def get_all_by_roteiro(db: Session, id_roteiro:int) -> List[RoteiroStage]:
        options = db.query(RoteiroStage).filter(RoteiroStage.id_roteiro == id_roteiro).all()
        if len(options) == 0:
            raise HTTPException(status_code=404, detail="Roteiro inexistente ou nenhum estágio encontrado")  
        return options
    
    def get_by_stage_and_roteiro(db: Session, stage: int, id_roteiro: int) -> List[RoteiroStage]:
        options = db.query(RoteiroStage).filter(RoteiroStage.stage == stage, RoteiroStage.id_roteiro == id_roteiro).all()
        if len(options) == 0:
            raise HTTPException(status_code=404, detail="Roteiro inexistente ou nenhum estágio dessa fase encontrado")  
        return options
    
    def get(db: Session, id_roteiroStage: int) -> RoteiroStage:
        option = db.query(RoteiroStage).filter(RoteiroStage.id_roteiroStage == id_roteiroStage).first()
        if option:
            return option
        raise HTTPException(status_code=404, detail="Opção do estágio não encontrado")

    def create(db: Session, stage: RoteiroStageIn) -> RoteiroStage:
        try:
            stage = RoteiroStage(**stage.model_dump())
            db.add(stage)
            db.commit()
            db.refresh(stage)
            return stage
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Erro ao criar estágio: {e}")

    def delete(db: Session, id_roteiroStage: int):
        rows_deleted = db.query(RoteiroStage).filter(RoteiroStage.id_roteiroStage == id_roteiroStage).delete()
        db.commit()
        if rows_deleted == 0:
            raise HTTPException(status_code=404, detail="Opção do estágio não encontrado")

    def delete_all_by_roteiro(db: Session, id_roteiro: int):
        rows_deleted = db.query(RoteiroStage).filter(RoteiroStage.id_roteiro == id_roteiro).delete()
        db.commit()
        if rows_deleted == 0:
            raise HTTPException(status_code=404, detail="Roteiro não encontrado")