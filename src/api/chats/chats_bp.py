from flask import Blueprint, jsonify, session, request
from flask_jwt_extended import jwt_required
from src.config.queries import *
from src.services.connection_db import ConnectionBD

chatsBp = Blueprint('chats', __name__)

@chatsBp.route('/user/chats', methods=['GET'])
@jwt_required()
def user_chats():
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'Error':'No hay ningún usuario logeado'}), 404
    
    try:
        connection = ConnectionBD()
        connection.connect()
        
        if connection.is_connected():
            print('Buscando chats del usuario ', user_id)
            
            chats = connection.select(
                'chats',
                ['id', 'user_id','name'],
                f"user_id = '{str(user_id)}'"
            )
            
        connection.disconnect()

        if not chats:
            return []
            
        return chats
        
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    
@chatsBp.route('/user/chat', methods=['POST'])
@jwt_required()
def insert_new_chat():
    user_id = session.get('user_id')
    chat_name = request.args.get('chat_name')
    
    if not user_id or not chat_name:
        return jsonify({'Error':'No hay ningún usuario logeado'}), 404
    
    try:
        connection = ConnectionBD()
        connection.connect()

        if connection.is_connected():
            print('Insertando chat nuevo para el usuario ', str(user_id))

            query = INSERT_CHAT(user_id, chat_name)
            print()
            print(query)
            print()
            chat_id = connection.set_query(query)

            connection.disconnect()

            if not chat_id:
                return jsonify({'Error': 'No se pudo obtener el id del chat'}), 500

            return jsonify({'chat_id': chat_id[0]}), 201  # Asumiendo que chat_id es una tupla
        
        return jsonify({'Error': 'No se pudo conectar a la base de datos'}), 500

    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    
