from fastapi import APIRouter, HTTPException, status # type: ignore

from typing import List
from .MessageDTO import MessageIn, MessageOut
from .Message import Message
from .MessageRepository import MessageRepository
from src.message.MessageAux import fetchData
from database import get_db

router = APIRouter()
db = get_db()

@router.get("/messages", response_model=None, tags=["message"])
def get_all(): 
    """Returns a Specific Message based on the id"""
    return list(MessageRepository.get_all(db))

@router.get("/messages/{id_conversation}")
def get_all_from_conversation(id_conversation: str):
    """Returns all messages from a Conversation"""
    return MessageRepository.get_by_conversation(db, id_conversation)

@router.post("/messages", response_model=MessageOut, status_code=status.HTTP_201_CREATED, tags=["message"])
def new_message(movIn : MessageIn):
    """Creates a New Message"""

    if not MessageRepository.check_by_conversation(db, movIn.id_conversation):
        message = MessageRepository.initialize_conversation(db, movIn).to_messageOut()
    return fetchData(movIn)

@router.delete("/messages/{id_conversation}", status_code=status.HTTP_204_NO_CONTENT, tags=["message"])
def deleta_conversation(id_conversation: str):
    """Deletes an entire Conversation's information"""
    return MessageRepository.delete_conversation(db, id_conversation)

@router.delete("/messages", status_code=status.HTTP_204_NO_CONTENT, tags=["message"])
def delete_all():
    return MessageRepository.delete_all(db)