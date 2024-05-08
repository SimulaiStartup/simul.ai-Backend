import dotenv
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from typing import List

import pandas as pd

from Message import Message
from MessageRepository import MessageRepository
from app.src.roteiro.RoteiroRepository import RoteiroRepository
from app.src.roteiroStage.RoteiroStageRepository import RoteiroStageRepository
from app.database import get_db

db = get_db()

dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("GPT_KEY")

# https://python.langchain.com/docs/expression_language/get_started/


MODEL = ChatOpenAI(model="gpt-4")


def fetchData(message: Message) -> str:

    

    # pegamos o contexto, ou seja, todas as mensagens trocadas até agora na conversa
    context = MessageRepository.get_by_conversation(db, message.id_conversation)

    # Pegamos o contexto do roteiro
    script = RoteiroRepository.get(db, message.id_roteiro)

    # O papel do chat no roteiro
    chat_role = script.chat

    # Pegamos a última etapa do roteiro
    stage = message.stage


    # Pegamos as opções da última etapa
    options = RoteiroStageRepository.get_by_stage_and_roteiro(db, stage, message.id_roteiro)

    # Construímos o prompt
    prompt = buildPrompt(context=context, df_scripts=df_script.iloc[0], message=user_response, chat_role=chat_role, options_qtty=len(options))

    # Pegamos a resposta do ChatGPT
    response = getResponse(options=options, prpt=prompt)

    # Salva a resposta do usuário e a do Chat na base de dados

    # Retorna a resposta do chat
    return options[response-1]



def buildPrompt(context: pd.DataFrame, roteiro: pd.Series, message:str, chat_role:str, options_qtty:int):

    prompt = "O contexto da Atividade para o usuário é:\n" + df_scripts["CONTEXT"] + "\n\n" + f"Você deve atuar como o {chat_role}" + "\n\n Essa é a conversa até agora: \n"

    messages = context['TRANSCRIPT'].to_list()
    senders = context['SENDER'].to_list()


    for i in range(len(context)):
        prompt += df_scripts[senders[i]] + " - " + messages[i] + "\n\n"

    prompt += "A última mensagem do/a " + df_scripts["USER"] + " foi:\n" + message + "\n\n"

    prompt+= "Qual seria a próxima resposta mais apropriada, entre as seguintes:\n"

    for i in range(options_qtty):
        prompt += f"{i+1} - " + "{Resposta " + f"{i+1}" + "}\n"

    prompt += "\nResponda SOMENTE com o número (1,2,3...) correspondente a resposta escolhida, em ordem"

    return prompt


def getResponse(options: List[str], prpt: str) -> int:

    prompt = ChatPromptTemplate.from_template(prpt)
    output_parser = StrOutputParser()

    chain = prompt | MODEL | output_parser

    n = chain.invoke({f"Resposta {i+1}":options[i] for i in range(len(options))})

    return int(n)

def main():
    print(fetchData(1, "Em ciência da computação, Hashmap é uma estrutura de dados especial que associa a chave de pesquisa a valores. Seu objetivo é a partir de uma chave simples, fazer uma busca rápida e obter o valor desejado. É algumas vezes traduzidas traduzida como tabela de dispersão."))

if __name__ == "__main__":
    main()