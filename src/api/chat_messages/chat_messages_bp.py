from flask import Blueprint, jsonify, session
from flask_jwt_extended import jwt_required
from src.config.queries import GET_CHAT_MESSAGES
from src.classes.postgres_connection_db import PostgresConnectionBD

chatMessagesBp = Blueprint('chat_messages', __name__)

@chatMessagesBp.route('/user/chat/<id>/messages', methods=['GET'])
@jwt_required()
def get_chat_messages(id):
    """
    Obtiene los mensajes de un chat.

    Args:
        id (str): ID del chat.

    Returns:
        jsonify: Mensajes del chat.
    """
    if not id:
        return jsonify({'Error':'No hay ningún chat con ese id'}), 404

    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'Error':'No hay ningún usuario logeado'}), 404
    
    try:

        connection = PostgresConnectionBD()
        connection.connect()
        
        if connection.is_connected():

            query = GET_CHAT_MESSAGES(chat_id=id, user_id=user_id)
            chat_messages = connection.set_query(query)

        connection.disconnect()

        if not chat_messages:
            return jsonify([])
        
        return jsonify(chat_messages)

    except Exception as e:
        return jsonify({'Error': str(e)}), 500
