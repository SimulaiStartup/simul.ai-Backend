from fastapi import APIRouter, HTTPException, status

from typing import List

from src.services.AudioService import speech_to_text
from src.services.MessageService import fetchData

from pydantic import BaseModel

router = APIRouter()

@router.get("/conversation/")
def conversation():
    return ""

class RequestBody(BaseModel):
    URL: str

@router.post("/conversation/{conversa_id}/{roteiro_id}", response_model=str)
def process_and_answer(conversa_id: int, roteiro_id: int, body: RequestBody):
    user_response = speech_to_text(body.URL)
    return fetchData(conversa_id, roteiro_id, user_response)

@router.post("youtube/", response_model=str)
def youtube():
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"