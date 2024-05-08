from pydantic import BaseModel

class RoteiroIn(BaseModel):
    context: str 
    chat: str 
    user: str


class RoteiroOut(BaseModel):
    id_roteiro: int 
    context: str 
    chat: str 
    user: str 