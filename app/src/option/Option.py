from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from .OptionDTO import OptionOut

from database import Base

class Option(Base):
    __tablename__ = "options"

    id_option =  Column(Integer, primary_key=True, index=True)
    tag =  Column(String)
    text = Column(String)
    video = Column(String)
    id_roteiro = Column(Integer, ForeignKey("roteiros.id_roteiro"))

    def to_optionOut(self) -> OptionOut:
        return OptionOut(
            id_option=self.id_option,
            tag=self.tag,
            text=self.text,
            id_roteiro=self.id_roteiro,
            video=self.video
        )