from typing import List
from pydantic import BaseModel


class OptionIn(BaseModel):
    id_roteiro: int 
    tag: str 
    text: str 
    video: str


class OptionOut(BaseModel):
    id_option: int
    id_roteiro: int 
    tag: str 
    text: str 
    video: str