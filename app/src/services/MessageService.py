import dotenv
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from typing import List

import pandas as pd

dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("GPT_KEY")

# https://python.langchain.com/docs/expression_language/get_started/


MODEL = ChatOpenAI(model="gpt-4")


def fetchData(conversa_id:int, roteiro_id:int, user_response:str) -> str:

    # df_messages é o dataframe com as mensagens referentes a conversa atual  
    df_messages = pd.read_csv("../../data/transcripts.csv", sep=";", encoding="UTF-8")

    # df_script é o dataframe com os roteiros
    df_script = pd.read_csv("../../data/roteiros.csv", sep=";", encoding="UTF-8")

    # df_script_stages é o dataframe com as etapas dos roteiros
    df_script_stages = pd.read_csv("../../data/roteiro_stages.csv", sep=";", encoding="UTF-8")

    # pegamos o contexto, ou seja, todas as mensagens trocadas até agora na conversa
    context = df_messages[df_messages['CONVERSATION_ID'] == conversa_id]

    # se o contexto é vazio, pegamos a primeira mensagem do roteiro
    if len(context) == 0:
        first_message = df_script_stages[(df_script_stages['ROTEIRO_ID'] == roteiro_id) & (df_script_stages['STAGE'] == 0)]
        first_message = {
            "CONVERSATION_ID" : [conversa_id], 
            "ROTEIRO_ID" : [roteiro_id], 
            "STAGE" : [0], 
            "MENSAGEM_ID" : [1], 
            "TRANSCRIPT" : [first_message['OPTION'].values[0]], 
            "SENDER": ["CHAT"]
        }
        df_messages = pd.concat([df_messages, pd.DataFrame(first_message)], ignore_index=True)
        df_messages.to_csv('data/conversation.csv', index=False, sep=";")
        context = df_messages[df_messages['CONVERSATION_ID'] == conversa_id]


    df_script = df_script[df_script['ROTEIRO_ID'] == roteiro_id]

    prompt = buildPrompt(context=context, df_scripts=df_script.iloc[0], message=user_response)

    stage = context['STAGE'].max()
    m_id = context['MENSAGEM_ID'].max()


    df_script_stages = df_script_stages[(df_script_stages['ROTEIRO_ID'] == roteiro_id) & (df_script_stages['STAGE'] == stage)]
    options = df_script_stages['OPTION'].astype(str).to_list()

    response = getResponse(options=options, prpt=prompt)

    print(response)
    print(options[response-1])

    data = {
        "CONVERSATION_ID" : [conversa_id, conversa_id], 
        "ROTEIRO_ID" : [roteiro_id, roteiro_id], 
        "STAGE" : [stage, stage], 
        "MENSAGEM_ID" : [m_id+1, m_id+2], 
        "TRANSCRIPT" : [user_response, options[response-1]], 
        "SENDER": ["USER", "CHAT"]
    }


    user_and_chat_answers = pd.DataFrame(data)
    df_messages = pd.concat([df_messages, user_and_chat_answers], ignore_index=True)
    df_messages.to_csv('data/conversation.csv', index=False, sep=";")

    return response



def buildPrompt(context: pd.DataFrame, df_scripts: pd.Series, message:str, chat_role:str):

    prompt = "O contexto da Atividade é:" + df_scripts["CONTEXT"] + "\n" + f"Você deve atuar como o {chat_role}" + "\n\n Essa é a conversa até agora: \n"

    messages = context['TRANSCRIPT'].to_list()
    senders = context['SENDER'].to_list()


    for i in range(len(context)):
        prompt += df_scripts[senders[i]] + " - " + messages[i] + "\n\n"

    prompt += "A última mensagem do/a " + df_scripts["USER"] + " foi:\n" + message

    prompt+= '''
Qual seria a próxima resposta mais apropriada, entre as seguintes:

    {Resposta1}

    {Resposta2}

    {Resposta3}

Responda somente com um número, correspondente a resposta escolhida
    '''

    return prompt


def getResponse(options: List[str], prpt: str) -> int:

    prompt = ChatPromptTemplate.from_template(prpt)
    output_parser = StrOutputParser()

    chain = prompt | MODEL | output_parser

    n = chain.invoke({f"Resposta{i+1}":options[i] for i in range(len(options))})

    return int(n)