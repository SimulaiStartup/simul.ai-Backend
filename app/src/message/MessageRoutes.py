from fastapi import APIRouter, HTTPException, status # type: ignore

from typing import List
from .MessageDTO import MessageIn, MessageOut
from .Message import Message
from .MessageRepository import MessageRepository
from src.message.MessageAux import fetchData
from database import get_db

router = APIRouter()
db = get_db()

@router.get("/messages/{id_message}", response_model=List[str], tags=["message"])
def get_message(id_message: int = None): 
    """Returns a Specific Message based on the id"""
    if id_message:
        return [MessageRepository.get(db,id_message).map(lambda x: (x.transcript, x.sender))]
    else:
        return MessageRepository.get_all(db).map(lambda x: (x.transcript, x.sender))

@router.post("/messages", response_model=MessageOut, status_code=status.HTTP_201_CREATED, tags=["message"])
def new_message(movIn : MessageIn):
    """Creates a New Message"""

    if MessageRepository.check_by_conversation(db, movIn.id_conversation):
        return MessageRepository.create_user_message(db, movIn)
    
    message = MessageRepository.create_conversation(db, movIn)
    return fetchData(message)

@router.delete("/messages/{id_message}", status_code=status.HTTP_204_NO_CONTENT, tags=["message"])
def deleta_message(id_message: int):
    """Deletes a Message's information"""
    return MessageRepository.delete(db,id_message)

@router.delete("/messages/conversation/{id_conversation}", status_code=status.HTTP_204_NO_CONTENT, tags=["message"])
def deleta_conversation(id_conversation: int):
    """Deletes an entire Conversation's information"""
    return MessageRepository.delete_conversation(db,id_conversation)