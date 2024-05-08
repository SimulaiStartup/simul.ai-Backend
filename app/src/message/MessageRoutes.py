from fastapi import APIRouter, HTTPException, status # type: ignore

from typing import List
from .MessageDTO import MessageIn, MessageOut
from .Message import Message
from .MessageRepository import MessageRepository
from database import get_db

router = APIRouter()
db = get_db()

@router.get("/message/{id_message}", response_model=List[Message], tags=["message"])
def get_message(id_message: int = None): 
    """Returns a Specific Message based on the id for the move and the Package id"""
    if id_message:
        return [MessageRepository.get(db,id_message)]
    else:
        return MessageRepository.get_all(db)

@router.post("/message", response_model=MessageOut, status_code=status.HTTP_201_CREATED, tags=["message"])
def new_message(movIn : MessageIn):
    """Creates a New Message"""

    
    return MessageRepository.create(db,movIn).map(lambda x: x)

@router.delete("/message/{id_message}", status_code=status.HTTP_204_NO_CONTENT, tags=["message"])
def deleta_message(id_message: int):
    """Deletes a Message's information"""
    return MessageRepository.delete(db,id_message)

@router.delete("/message/conversation/{id_conversation}", status_code=status.HTTP_204_NO_CONTENT, tags=["message"])
def deleta_message(id_conversation: int):
    """Deletes an entire Conversation's information"""
    return MessageRepository.delete_conversation(db,id_conversation)