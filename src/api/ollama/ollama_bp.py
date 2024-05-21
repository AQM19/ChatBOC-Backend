from flask import Blueprint, jsonify, request

from utils.Utils import Utils
from src.services.BaseService import BaseService

ollamaBp = Blueprint('ollama', __name__)


@ollamaBp.route('/', methods=['GET'])
def ask() -> str:
    question = request.args.get('question', default='tell me a joke')
    try:
        base_service = BaseService()
        response = base_service.manage_response(question)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return response
