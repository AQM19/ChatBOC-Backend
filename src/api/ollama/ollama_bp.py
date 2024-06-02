from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import jwt_required
from src.config.queries import INSERT_QUESTION, INSERT_RESPONSE
from src.classes.postgres_connection_db import PostgresConnectionBD
from src.services.model_service import ModelService

ollamaBp = Blueprint('ollama', __name__)

@ollamaBp.route('/', methods=['GET'])
@jwt_required()
def ask() -> str:
    """
    Maneja las solicitudes de preguntas al modelo de IA.

    Returns:
        str: Respuesta del modelo de IA.
    """
        
    user_id = session.get('user_id')
    question = request.args.get('question')
    chat_id = request.args.get('chat_id')

    try:
        
        if not user_id:
            return jsonify({'Error': 'No hay ninún usuario logeado'}), 404
        
        if not chat_id:
            return jsonify({'Error': 'No hay ninún chat seleccionado'}), 404

        connection = PostgresConnectionBD()
        connection.connect()

        if connection.is_connected():

            query = INSERT_QUESTION(chat_id, user_id, question)
            connection.set_query_and_no_return(query)

        connection.disconnect()

        base_service = ModelService()
        response = base_service.manage_response(question)

        connection.connect()
        
        if connection.is_connected():

            query = INSERT_RESPONSE(chat_id, user_id, response)
            connection.set_query_and_no_return(query)

        connection.disconnect()
        
        return response
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500