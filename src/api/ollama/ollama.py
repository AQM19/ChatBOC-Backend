from flask import Blueprint, request

from utils.Utils import Utils
from src.services.BaseService import BaseService

ollamaBp = Blueprint('ollama', __name__)

base_service = BaseService()

@ollamaBp.route('/', methods=['GET'])
def ask() -> str:
    question = request.args.get('question', default='tell me a joke')
    response = base_service.manage_response(question)
    return response
