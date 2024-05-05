from fastapi import APIRouter, HTTPException, status

from typing import List

from src.services.AudioService import speech_to_text
from src.services.MessageService import fetchData

router = APIRouter()

@router.get("/conversation/")
def conversation():
    return ""

@router.get("/conversation/{conversa_id}/{roteiro_id}/{URL}", response_model=str, tags=["audio"])
def process_and_answer(conversa_id: int, roteiro_id: int, URL: str):
    user_response = speech_to_text(URL)
    return fetchData(conversa_id, roteiro_id, user_response)