from pydantic import BaseModel


class MessageIn(BaseModel):
    id_conversation: str
    id_roteiro: int
    url: str
    sender: str | None = "user"


class MessageOut(BaseModel):
    link: str
    end: bool