from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database import Base


class Message(Base):
    __tablename__ = "messages"

    id_conversation =  Column(String, primary_key=True, index=True)
    id_message =  Column(Integer, primary_key=True, index=True)
    id_roteiro = Column(Integer, ForeignKey("roteiros.id_roteiro"))
    stage = Column(Integer)
    transcript = Column(String)
    sender = Column(Boolean, default=True)


