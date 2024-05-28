import dotenv
import os
from fastapi import HTTPException
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from typing import List, Dict, Tuple

import re


from src.message.MessageRepository import MessageRepository
from src.roteiro.RoteiroRepository import RoteiroRepository
from src.roteiro.Roteiro import Roteiro
from src.checklist.ChecklistRepository import ChecklistRepository
from src.checklist.ChecklistDTO import FeedbackOut
from database import get_db

db = get_db()

dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("GPT_KEY")

MODEL = ChatOpenAI(model="gpt-4")


def feedback(roteiro: Dict, context:List[Tuple[bool, str]]):

    prpt = "O contexto da Atividade para o usuário é:\n" + roteiro["context"] + "\n\n" + f"Ele está comunicando com {roteiro['chat']}" + "\n\n Essa é a conversa até agora: \n"

    senders = ["user" if x[0] else "chat" for x in context]
    messages = [x[1] for x in context]


    for i in range(len(context)):
        prpt += roteiro[senders[i]] + " - " + messages[i] + "\n\n"

    prpt += f'''
        \nAvalie o {roteiro['user']} baseado nos seguintes critérios:
    '''

    for cl in ChecklistRepository.get_all_checklists_by_roteiro(db, roteiro['id_roteiro']):
        prpt += '\n ' + cl.question + ' \n'

    prpt += '\n {question}'

    prompt = ChatPromptTemplate.from_template(prpt)
    output_parser = StrOutputParser()

    chain = prompt | MODEL | output_parser

    n = chain.invoke({f"question":"Retorne uma avaliação separada por critério, mostrando detalhadamente o que foi atingido e o que não foi para cada um."})

    return n


def fetchFeedback(id_conversation: str) -> str:

    # pegamos o contexto, ou seja, todas as mensagens trocadas até agora na conversa
    if MessageRepository.check_by_conversation(db, id_conversation):
        context = MessageRepository.get_by_conversation(db, id_conversation)
    else:
        return HTTPException(status_code=404, detail="Conversa não encontrada")

    print("pegando o id do roteiro")
    id_roteiro = context[0].id_roteiro

    print("construindo o prompt")
    full_context = [(message.sender, message.transcript) for message in context]

    print("pegando o roteiro")
    # Pegamos o contexto do roteiro
    script = Roteiro.to_roteiroOut(RoteiroRepository.get(db, id_roteiro))

    print("pegando a próxima etapa")
    # Pegamos a próxima etapa da conversa
    f = feedback(script.model_dump(), full_context)

    return FeedbackOut(
        id_conversation=id_conversation, 
        feedback=f
    )