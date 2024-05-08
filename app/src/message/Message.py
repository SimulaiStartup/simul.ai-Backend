from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.src.message.MessageAux import fetchData
from database import Base

from MessageDTO import MessageOut

class Message(Base):
    __tablename__ = "messages"

    id_conversation =  Column(Integer, primary_key=True, index=True)
    id_message =  Column(Integer, primary_key=True, index=True)
    id_roteiro = Column(Integer, ForeignKey("roteiros.id_roteiro"))
    stage = Column(Integer)
    transcript = Column(String)
    sender = Column(Boolean, default=True)


    def to_MessageOut(self) -> MessageOut:


        return MessageOut(
            link = fetchData(self)
        )

