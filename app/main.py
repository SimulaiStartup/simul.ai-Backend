# run: uvicorn main:app --reload

from fastapi import FastAPI # type: ignore
from typing import List
from src import ConversationController

app = FastAPI()
app.include_router(ConversationController.router)

@app.get("/")
def root():
    return {"Hello": "World"}