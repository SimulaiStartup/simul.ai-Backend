from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.message import MessageRoutes
from src.roteiro import RoteiroRoutes
from src.roteiroStage import RoteiroStageRoutes
from database import engine, Base
from src.services.AudioService import speech_to_text
from src.message.MessageAux import fetchData
from src.message.MessageDTO import MessageIn
from src.message.MessageDTO import MessageOut
from pydantic import BaseModel

# Cria todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, you can restrict this to specific domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allow only specific HTTP methods
    allow_headers=["*"],  # Allow all headers, you can restrict this as needed
)

# Include your router
app.include_router(MessageRoutes.router)
app.include_router(RoteiroRoutes.router)
app.include_router(RoteiroStageRoutes.router)

# Define root route handler
@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/conversation", response_model=MessageOut)
def process_and_answer(body: MessageIn):
    #body.url = speech_to_text(body.url)
    return fetchData(body)