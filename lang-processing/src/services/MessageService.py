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


def fetchData(message:str, id:int) -> str:

    df_messages = pd.read_csv("../../data/transcripts.csv", sep=";", encoding="UTF-8")

    context = df_messages[df_messages['CONVERSATION_ID'] == id]

    id_script = context['ROTEIRO_ID'].iloc[0]

    df_script = pd.read_csv("../../data/roteiros.csv", sep=";", encoding="UTF-8")

    df_script = df_script[df_script['ROTEIRO_ID'] == id_script]

    prompt = buildPrompt(context=context, df_scripts=df_script.iloc[0], message=message)

    stage = context['STAGE'].max()+1
    m_id = context['MENSAGEM_ID'].max()


    df_script_stages = pd.read_csv("../../data/roteiro_stages.csv", sep=";", encoding="UTF-8")

    df_script_stages = df_script_stages[df_script_stages['ROTEIRO_ID'] == id_script]

    options = df_script_stages[df_script_stages['STAGE'] == stage]
    options = options['OPTION'].astype(str).to_list()

    response = getResponse(options=options, prpt=prompt)

    print(response)
    print(options[response-1])

    data = {
        "CONVERSATION_ID" : [id, id], 
        "ROTEIRO_ID" : [id_script, id_script], 
        "STAGE" : [stage, stage], 
        "MENSAGEM_ID" : [m_id+1, m_id+2], 
        "TRANSCRIPT" : [message, options[response-1]], 
        "SENDER": ["USER", "CHAT"]
    }


    df = pd.DataFrame(data)

    print(df.head())
    
    df.to_csv('../../data/transcripts.csv', mode='a', index=False, header=False, sep=";")

    return response



def buildPrompt(context: pd.DataFrame, df_scripts: pd.Series, message:str):

    prompt = df_scripts["CONTEXT"] + "\n\n Essa é a conversa até agora: \n"

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