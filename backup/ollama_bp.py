from flask import Blueprint, jsonify, request, stream_with_context, Response


from utils.Utils import Utils
from src.services.model_service import ModelService

ollamaBp = Blueprint('ollama', __name__)

@ollamaBp.route('/', methods=['GET'])
def ask() -> str:
    question = request.args.get('question')
    
    try:
        base_service = ModelService()
        response = base_service.manage_response(question)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return response
    
@ollamaBp.route('/stream', methods=['POST'])
def ask_stream() -> str:
    question = request.args.get('question')
    
    try:
        return Response(stream_with_context(Utils.stream_from_the_llama(message=question)), mimetype='aplicatioon/json')
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    