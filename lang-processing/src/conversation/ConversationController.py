from fastapi import APIRouter, HTTPException, status

from typing import List

from AudioService import speech_to_text

router = APIRouter()

@router.get("/answer/", response_model=str, tags=["audio"])
def process_and_answer(URL: str):
    response = speech_to_text(URL)
    return response