from sqlalchemy.orm import Session
from fastapi import HTTPException

from .Option import Option
from .OptionDTO import OptionIn
from typing import List

class OptionRepository:
    #def get(db: Session, id_option: int) -> Option:
        #roteiro_stages = db.query(Option).filter(Option.id_option == id_option).all()
        #if roteiro_stages:
            #return roteiro_stages
        #raise HTTPException(status_code=404, detail="Roteiro Inexistente ou Nenhum Estágio Encontrado")
    
    def get_all_by_roteiro(db: Session, id_roteiro:int) -> List[Option]:
        options = db.query(Option).filter(Option.id_roteiro == id_roteiro).all()
        if len(options) == 0:
            raise HTTPException(status_code=404, detail="Roteiro inexistente ou nenhuma opção encontrada")  
        return options
    
    def get_by_tag_and_roteiro(db: Session, tag: str, id_roteiro: int) -> List[Option]:
        options = db.query(Option).filter(Option.tag == tag, Option.id_roteiro == id_roteiro).all()
        if len(options) == 0:
            raise HTTPException(status_code=404, detail="Roteiro inexistente ou nenhum tag encontrada")  
        return options
    
    def get_tags_by_roteiro(db: Session, id_roteiro: int) -> List[Option]:
        options = OptionRepository.get_all_by_roteiro(db, id_roteiro)
        if len(options) == 0:
            raise HTTPException(status_code=404, detail="Roteiro inexistente ou nenhum tag encontrada")  
        
        return set(map(lambda x: x.tag, options))
    
    def get(db: Session, id_option: int) -> Option:
        option = db.query(Option).filter(Option.id_option == id_option).first()
        if option:
            return option
        raise HTTPException(status_code=404, detail="Opção não encontrada")

    def create(db: Session, stage: OptionIn) -> Option:
        try:
            stage = Option(**stage.model_dump())
            db.add(stage)
            db.commit()
            db.refresh(stage)
            return stage
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Erro ao criar opção: {e}")

    def delete(db: Session, id_option: int):
        rows_deleted = db.query(Option).filter(Option.id_option == id_option).delete()
        db.commit()
        if rows_deleted == 0:
            raise HTTPException(status_code=404, detail="Opção não encontrada")

    def delete_all_by_roteiro(db: Session, id_roteiro: int):
        rows_deleted = db.query(Option).filter(Option.id_roteiro == id_roteiro).delete()
        db.commit()
        if rows_deleted == 0:
            raise HTTPException(status_code=404, detail="Roteiro não encontrado")