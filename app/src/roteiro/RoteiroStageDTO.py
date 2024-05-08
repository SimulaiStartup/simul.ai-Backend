from pydantic import BaseModel


class RoteiroStageIn(BaseModel):
    id_roteiro: int 
    stage: str 
    option: str 


class RoteiroStageOut(BaseModel):
    id_roteiroStage: int 
    id_roteiro: int 
    stage: str 
    option: str 
