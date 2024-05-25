from flask import Blueprint, jsonify, session, request
from flask_jwt_extended import jwt_required
from src.config.queries import *
from src.services.connection_db import ConnectionBD

chatMessagesBp = Blueprint('chat_messages', __name__)

@chatMessagesBp.route('/user/chat/messages', methods=['GET'])
@jwt_required()
def get_chat_messages():
    user_id = session.get('user_id')
    chat_id = request.args.get('chat_id')
    
    if not user_id and not chat_id:
        return jsonify({'Error':'No hay ningún usuario logeado'}), 404
    
    try:

        connection = ConnectionBD()
        connection.connect()
        
        if connection.is_connected():

            chat_messages = connection.select(
                'chat_messages',
                ['id', 'chat_id', 'user_id', 'message'],
                f"user_id = '{str(user_id)}' and chat_id = '{str(chat_id)}'"
            )
        connection.disconnect()

        if not chat_messages:
            return []
        
        return chat_messages

    except Exception as e:
        return jsonify({'Error': str(e)}), 500