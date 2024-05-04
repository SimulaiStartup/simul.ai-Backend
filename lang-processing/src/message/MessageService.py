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

    prompt = buildPrompt(context=context, df_scripts=df_script, message=message)


    stage = context['STAGE'].max()+1

    print(stage)

    df_script_stages = pd.read_csv("../../data/roteiro_stages.csv", sep=";", encoding="UTF-8")

    df_script_stages = df_script_stages[df_script_stages['ROTEIRO_ID'] == id_script]

    options = df_script_stages[df_script_stages['STAGE'] == stage]
    options = options['OPTION'].astype(str).to_list()

    print(options)


    return getResponse(options=options, prpt=prompt)



def buildPrompt(context: pd.DataFrame, df_scripts: pd.DataFrame, message:str):

    prompt = df_scripts["CONTEXT"].to_string() + "\n\n Essa é a conversa até agora: \n"

    messages = context['TRANSCRIPT'].to_list()
    senders = context['SENDER'].to_list()


    for i in range(len(context)):
        prompt += df_scripts[senders[i]].to_string() + " - " + messages[i] + "\n\n"

    prompt += "A última mensagem do/a " + df_scripts["USER"].to_string() + " foi:\n" + message

    prompt+= '''
Qual seria a próxima resposta mais apropriada, entre as seguintes:

    {Resposta1}

    {Resposta2}

    {Resposta3}

Responda somente com um número, correspondente a resposta escolhida
    '''

    return prompt


def getResponse(options: List[str], prpt: str) -> str:

    prompt = ChatPromptTemplate.from_template(prpt)
    output_parser = StrOutputParser()

    chain = prompt | MODEL | output_parser

    return chain.invoke({f"Resposta{i+1}":options[i] for i in range(len(options))})