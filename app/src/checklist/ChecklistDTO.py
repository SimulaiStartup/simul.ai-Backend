from typing import List
from pydantic import BaseModel


class ChecklistIn(BaseModel):
    id_roteiro: int 
    text: List[str] 


class ChecklistOut(BaseModel):
    id_checklist: str
    id_roteiro: int
    text: str
