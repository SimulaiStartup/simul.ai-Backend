from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from .RoteiroDTO import RoteiroOut
from typing import List

from database import Base
from datetime import datetime

class Roteiro(Base):
    __tablename__ = "roteiros"

    id_roteiro =  Column(Integer, primary_key=True, index=True)
    context = Column(String)
    chat = Column(String)
    user = Column(String)


    def to_roteiroOut(self) -> RoteiroOut:
        return RoteiroOut(
            id_roteiro=self.id_roteiro,
            context=self.context,
            chat=self.chat,
            user=self.user
        )