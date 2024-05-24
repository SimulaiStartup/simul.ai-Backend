from typing import List
from pydantic import BaseModel


class ChecklistIn(BaseModel):
    id_roteiro: int 
    list_questions: List[str] 

class ChecklistCreate(BaseModel):
    id_roteiro: int 
    question: str 


class ChecklistOut(BaseModel):
    id_checklist: str
    id_roteiro: int
    question: str
