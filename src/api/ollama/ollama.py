from flask import Blueprint, request

from utils.Utils import Utils

ollamaBp = Blueprint('ollama', __name__)

@ollamaBp.route('/', methods=['GET'])
def ask() -> str:
    question = request.args.get('question', default='tell me a joke')
    response = Utils.ask_to_the_llama(question)
    return response['message']['content']
