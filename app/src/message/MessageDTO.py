from pydantic import BaseModel


class MessageIn(BaseModel):
    id_conversation: int 
    id_roteiro: int
    url: str
    sender: str | None = "USER"


class MessageOut(BaseModel):
    link: str
