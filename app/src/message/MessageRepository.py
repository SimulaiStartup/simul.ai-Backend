from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.message.Message import Message
from src.message.MessageDTO import MessageIn
from src.option.OptionRepository import OptionRepository
from typing import List
from datetime import datetime

class MessageRepository:

    def get_all(db: Session) -> List[Message]:
        messages = db.query(Message).all()
        return messages
    
    def get_by_conversation(db: Session, id_conversation: int) -> List[Message]:
        messages = db.query(Message).filter(Message.id_conversation == id_conversation).all()
        if len(messages) == 0:
            raise HTTPException(status_code=404, detail="Nenhuma mensagem encontrada pra essa conversa")  
        return messages
    
    def get_by_roteiro(db: Session, id_roteiro: int) -> List[Message]:
        messages = db.query(Message).filter(Message.id_roteiro == id_roteiro).all()
        if len(messages) == 0:
            raise HTTPException(status_code=404, detail="Nenhuma mensagem encontrada pra esse roteiro")  
        return messages
    
    def check_by_conversation(db: Session, id_conversation: int) -> bool:
        messages = db.query(Message).filter(Message.id_conversation == id_conversation).all()
        if len(messages) == 0:
            return False 
        return True

    def initialize_conversation(db: Session, message: MessageIn) -> Message:
        message = Message(
            id_message = 0,
            id_conversation = message.id_conversation,
            id_roteiro = message.id_roteiro,
            tag = 'Init',
            transcript = OptionRepository.get_by_stage_and_roteiro(db, 0, message.id_roteiro)[0].option,
            sender = False,
            data = message.data
        )
        db.add(message)
        db.commit()
        db.refresh(message)

        return message
    
    def create_user_message(db: Session, message: MessageIn, tag: str) -> Message:
        message = Message(
            id_message = MessageRepository.get_next_message_by_conversation(db, message.id_conversation),
            id_conversation = message.id_conversation,
            id_roteiro = message.id_roteiro,
            tag = tag,
            transcript = message.url,
            sender = True,
            data = message.data
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    def create_chat_message(db: Session, id_conversation: int, id_roteiro: int, option: str, tag:str) -> Message:
        message = Message(
            id_message = MessageRepository.get_next_message_by_conversation(db, id_conversation),
            id_conversation = id_conversation,
            id_roteiro = id_roteiro,
            tag = tag,
            transcript = option,
            sender = False,
            data = datetime.now()
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
        
    def delete_conversation(db: Session, id_conversation: int):
        rows_deleted = db.query(Message).filter(Message.id_conversation == id_conversation).delete()
        db.commit()
        if rows_deleted == 0:
            raise HTTPException(status_code=404, detail="Message não encontrada")
    
    
    
    def get_next_message_by_conversation(db : Session, id_conversation : int) -> int:
        messages = MessageRepository.get_by_conversation(db, id_conversation)

        id_message = messages[-1].id_message + 1

        return id_message
    
    def delete_all(db: Session):
        rows_deleted = db.query(Message).delete()
        db.commit()
        if rows_deleted == 0:
            raise HTTPException(status_code=404, detail="Message não encontrada")