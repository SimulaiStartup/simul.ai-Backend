from flask import Flask, request, jsonify

from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)
load_dotenv()
model = ChatOpenAI(openai_api_key=os.getenv('GPT_KEY'), model="gpt-4")

@app.route('/')
def home():
    return 'Hello World!'

@app.route('/audio', methods=['POST'])
def receive_and_process_audio():
    try:
        audio = request.get_json()['audio']
    except:
        return jsonify({'error': 'Invalid JSON'}), 400




@app.route('/gpt', methods=['POST'])
def comunicate_with_gpt():
    try:
        item = request.get_json()
    except:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    if 'prompt' not in item:
        return jsonify({'error': 'No prompt provided'}), 400
    
    prompt = item['prompt']
    ChatPromptTemplate.from_template(prompt)
    output_parser = StrOutputParser()