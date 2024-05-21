import dotenv
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from typing import List, Dict

import pandas as pd


from src.message.Message import Message
from src.message.MessageDTO import MessageIn, MessageOut
from src.message.MessageRepository import MessageRepository
from src.roteiro.RoteiroRepository import RoteiroRepository
from src.roteiro.Roteiro import Roteiro
from src.roteiro.RoteiroDTO import RoteiroOut
from src.option.OptionRepository import OptionRepository
from database import get_db

db = get_db()

dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("GPT_KEY")

# https://python.langchain.com/docs/expression_language/get_started/


MODEL = ChatOpenAI(model="gpt-4")


def fetchNextTag(transcript: str, roteiro: Dict, context:List[str]):

    prpt = "O contexto da Atividade para o usuário é:\n" + roteiro["context"] + "\n\n" + f"Você deve atuar como o {roteiro['chat']}" + "\n\n Essa é a conversa até agora: \n"

    senders = ["user" if x[0] else "chat" for x in context]
    messages = [x[1] for x in context]


    for i in range(len(context)):
        prpt += roteiro[senders[i]] + " - " + messages[i] + "\n\n"

    prpt += f'''
        \nDada a mensagem '{transcript}' vindo do {roteiro['user']}, qual dessas opções é mais condizente com o que foi perguntado:
    '''

    for tag in OptionRepository.get_tags_by_roteiro(db, roteiro['id_roteiro']):
        prpt += '\n ' + tag + ' \n'

    prpt += '\n {question}'

    prompt = ChatPromptTemplate.from_template(prpt)
    output_parser = StrOutputParser()

    chain = prompt | MODEL | output_parser

    n = chain.invoke({f"question":'Retorne apenas a opção, da mesma maneira que ela foi escrita'})

    return n





def fetchData(message: MessageIn) -> str:
    print("começo")
    # pegamos o contexto, ou seja, todas as mensagens trocadas até agora na conversa
    if MessageRepository.check_by_conversation(db, message.id_conversation):
        context = MessageRepository.get_by_conversation(db, message.id_conversation)
    else:
        # se a conversa tiver acabado de começar, inicializamos ela
        context = [MessageRepository.initialize_conversation(db, message)]

    print("construindo o prompt")
    full_context = [(message.sender, message.transcript) for message in context]

    print("pegando o roteiro")
    # Pegamos o contexto do roteiro
    script = Roteiro.to_roteiroOut(RoteiroRepository.get(db, message.id_roteiro))

    print("pegando a próxima etapa")
    # Pegamos a próxima etapa da conversa
    next_tag = fetchNextTag(message.url, script.model_dump(), full_context)

    print("pegando as opções")
    # Pegamos as opções da última etapa
    options_roteiro = OptionRepository.get_by_tag_and_roteiro(db, next_tag, message.id_roteiro)
    options = [option.text for option in options_roteiro]


    print("pegando o prompt")
    # Construímos o prompt
    prompt = buildPrompt(context=full_context, roteiro=script.model_dump(), message=message.url, options_qtty=len(options))
    print(prompt)

    # Pegamos a resposta do ChatGPT
    response = getResponse(options=options, prpt=prompt)
    print("Resposta do Chat: " + str(response))

    if response == -1:
        failed_response = OptionRepository.get_by_tag_and_roteiro(db, 'Confusão', message.id_roteiro)[0]
        return MessageOut(link = failed_response.video, end=False)

    # Salva a resposta do usuário e a do Chat na base de dados
    MessageRepository.create_user_message(db, message, next_tag)

    # Salva a resposta do usuário e a do Chat na base de dados
    MessageRepository.create_chat_message(db, message.id_conversation, message.id_roteiro, options_roteiro[response-1].text,next_tag)

    # Retorna a resposta do chat
    if next_tag != 'END': return MessageOut(link = options_roteiro[response-1].video, end=False)

    return MessageOut(link = options_roteiro[response-1].video, end=True)



def buildPrompt(context: List[str], roteiro: Dict, message:str, options_qtty:int):

    prompt = "O contexto da Atividade para o usuário é:\n" + roteiro["context"] + "\n\n" + f"Você deve atuar como o {roteiro['chat']}" + "\n\n Essa é a conversa até agora: \n"

    senders = ["user" if x[0] else "chat" for x in context]
    messages = [x[1] for x in context]

    for i in range(len(context)):
        prompt += roteiro[senders[i]] + " - " + messages[i] + "\n\n"

    prompt += "A última mensagem do/a " + roteiro["user"] + " foi:\n" + message + "\n\n"

    prompt+= "Qual seria a próxima resposta mais apropriada, entre as seguintes:\n"

    for i in range(options_qtty):
        prompt += f"{i+1} - " + "{Resposta " + f"{i+1}" + "}\n"

    prompt += "\nResponda SOMENTE com o número (1,2,3...) correspondente a resposta escolhida. Se nenhuma das opções for minimamente adequada, responda com -1."

    return prompt


def getResponse(options: List[str], prpt: str) -> int:

    prompt = ChatPromptTemplate.from_template(prpt)
    output_parser = StrOutputParser()

    chain = prompt | MODEL | output_parser

    n = chain.invoke({f"Resposta {i+1}":options[i] for i in range(len(options))})

    return int(n)

def main():
    print(fetchData(MessageIn(id_conversation="teste1", id_roteiro=1, url="Bom Dia, eu sou um aluno")))

if __name__ == "__main__":
    main()