from pydantic import BaseModel
from datetime import datetime


class MessageIn(BaseModel):
    id_conversation: str
    id_roteiro: int
    url: str
    sender: str | None = "user"
    data: datetime = datetime.now()


class MessageOut(BaseModel):
    link: str
    end: bool