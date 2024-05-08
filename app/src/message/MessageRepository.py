from sqlalchemy.orm import Session
from fastapi import HTTPException

from .Message import Message
from .MessageDTO import MessageIn, MessageUpdate
from typing import List

class MessageRepository:

    def get(db: Session, id_message: int) -> Message:
        message = db.query(Message).filter(Message.id_message == id_message).first()
        if message:
            return message
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")

    def get_all(db: Session) -> List[Message]:
        messages = db.query(Message).all()
        return messages
    
    def get_by_conversation(db: Session, id_conversation: int) -> List[Message]:
        messages = db.query(Message).filter(Message.id_conversation == id_conversation).all()
        if len(messages) == 0:
            raise HTTPException(status_code=404, detail="Nenhuma conversa encontrada para o ID enviado")  
        return messages

    def create(db: Session, message: MessageIn) -> Message:
        message = Message(**message.model_dump())
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def delete(db: Session, id_message: int):
        rows_deleted = db.query(Message).filter(Message.id_message == id_message).delete()
        db.commit()
        if rows_deleted == 0:
            raise HTTPException(status_code=404, detail="Message não encontrada")
        
    def delete_conversation(db: Session, id_conversation: int):
        rows_deleted = db.query(Message).filter(Message.id_conversation == id_conversation).delete()
        db.commit()
        if rows_deleted == 0:
            raise HTTPException(status_code=404, detail="Message não encontrada")