from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.api.chats.chats_bp import insert_new_chat
from src.services.model_service import ModelService

ollamaBp = Blueprint('ollama', __name__)

@ollamaBp.route('/', methods=['GET'])
@jwt_required()
def ask() -> str:
    
    question = request.args.get('question')

    try:
        
        base_service = ModelService()
        response = base_service.manage_response(question)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return response