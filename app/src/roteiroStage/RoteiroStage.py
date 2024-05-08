from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from .RoteiroStageDTO import RoteiroStageOut

from database import Base

class RoteiroStage(Base):
    __tablename__ = "roteiroStages"

    id_roteiroStage =  Column(Integer, primary_key=True, index=True)
    stage =  Column(Integer)
    option = Column(String)
    id_roteiro = Column(Integer, ForeignKey("roteiros.id_roteiro"))

    def to_RoteiroStageOut(self) -> RoteiroStageOut:
        return RoteiroStageOut(
            id_roteiroStage=self.id_roteiroStage,
            stage=self.stage,
            option=self.option,
            id_roteiro=self.id_package,
        )