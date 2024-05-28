from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from .ChecklistDTO import ChecklistOut

from database import Base

class Checklist(Base):
    __tablename__ = "checklists"

    id_checklist =  Column(Integer, primary_key=True, index=True)
    question = Column(String)
    id_roteiro = Column(Integer, ForeignKey("roteiros.id_roteiro"))

    def to_checklistOut(self) -> ChecklistOut:
        return ChecklistOut(
            id_checklist=self.id_checklist,
            question=self.question,
            id_roteiro=self.id_roteiro
        )