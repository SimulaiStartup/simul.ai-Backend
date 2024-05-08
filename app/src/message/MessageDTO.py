from pydantic import BaseModel


class MessageIn(BaseModel):
    id_conversation: int 
    id_roteiro: int
    transcript: str
    sender: str | None = "CHAT"


class MessageOut(BaseModel):
    link: str
