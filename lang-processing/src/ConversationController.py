from fastapi import APIRouter, HTTPException, status

from typing import List

from services.AudioService import speech_to_text
from services.MessageService import fetchData

router = APIRouter()

@router.get("/answer/", response_model=str, tags=["audio"])
def process_and_answer(URL: str, id: int):
    response = speech_to_text(URL)
    return fetchData(response, id)