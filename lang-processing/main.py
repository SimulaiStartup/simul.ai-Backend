# run: uvicorn main:app --reload

from fastapi import FastAPI # type: ignore
from typing import List
from src.conversation import AudioController

app = FastAPI()
app.include_router(AudioController.router)

@app.get("/")
def root():
    return {"Hello": "World"}