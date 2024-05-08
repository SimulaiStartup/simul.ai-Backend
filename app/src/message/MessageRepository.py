from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.src.services.AudioService import speech_to_text

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
    
    def check_by_conversation(db: Session, id_conversation: int) -> bool:
        messages = db.query(Message).filter(Message.id_conversation == id_conversation).all()
        if len(messages) == 0:
            return False 
        return True

    def create_user_message(db: Session, message: MessageIn) -> Message:
        message = Message(
            id_message = MessageRepository.get_current_message_id_by_conversation(db, message.id_conversation),
            id_conversation = message.id_conversation,
            id_roteiro = message.id_roteiro,
            stage = MessageRepository.get_current_stage_by_conversation(db, message.id_conversation),
            transcript = speech_to_text(message.url),
            sender = message.sender
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    def create_chat_message(db: Session, message: MessageIn) -> Message:
        message = Message(
            id_message = MessageRepository.get_current_message_id_by_conversation(db, message.id_conversation),
            id_conversation = message.id_conversation,
            id_roteiro = message.id_roteiro,
            stage = MessageRepository.get_current_stage_by_conversation(db, message.id_conversation)-1,
            transcript = speech_to_text(message.url),
            sender = message.sender
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    def create_conversation(db: Session, message: MessageIn) -> Message:
        
        message = Message(
            id_message = 0,
            id_conversation = message.id_conversation,
            id_roteiro = message.id_roteiro,
            stage = 0,
            transcript = speech_to_text(message.url),
            sender = message.sender
        )
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
    
    def get_current_stage_by_conversation(db : Session, id_conversation : int):
        messages = MessageRepository.get_by_conversation(db, id_conversation)

        stage = messages.map(lambda x: x.stage).reduce(lambda x,y: max(x,y))

        return stage+1
    
    def get_current_message_id_by_conversation(db : Session, id_conversation : int):
        messages = MessageRepository.get_by_conversation(db, id_conversation)

        id_message = messages.map(lambda x: x.id_message).reduce(lambda x,y: max(x,y))

        return id_message+1
