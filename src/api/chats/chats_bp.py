from flask import Blueprint, jsonify, session, request
from flask_jwt_extended import jwt_required
from src.config.queries import *
from src.classes.postgres_connection_db import PostgresConnectionBD

chatsBp = Blueprint('chats', __name__)

@chatsBp.route('/user/chats', methods=['GET'])
@jwt_required()
def user_chats():
    """
    Obtiene todos los chats del usuario.

    Returns:
        jsonify: Lista de chats del usuario.
    """
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'Error':'No hay ningún usuario logeado'}), 404
    
    try:
        connection = PostgresConnectionBD()
        connection.connect()
        
        if connection.is_connected():
            print('Buscando chats del usuario ', user_id)
            
            chats = connection.select(
                'chats',
                ['id','name'],
                f"user_id = '{str(user_id)}'"
            )
            
            connection.disconnect()

            if not chats:
                return jsonify([])
            
            return jsonify(chats)
        
        return jsonify({'Error': 'No se pudo conectar a la base de datos'}), 500
            
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    
@chatsBp.route('/user/chat', methods=['POST'])
@jwt_required()
def insert_new_chat():
    """
    Inserta un nuevo chat para el usuario.

    Returns:
        jsonify: ID del chat insertado.
    """
    user_id = session.get('user_id')
    chat_name = request.json.get('chat_name')
    
    print()
    print(chat_name)
    print()
    
    if not user_id or not chat_name:
        return jsonify({'Error':'No hay ningún usuario logeado'}), 404
    
    try:
        connection = PostgresConnectionBD()
        connection.connect()

        if connection.is_connected():
            print('Insertando chat nuevo para el usuario ', str(user_id))

            query = INSERT_CHAT(user_id, chat_name)
            chat_id = connection.set_query(query)

            connection.disconnect()

            if not chat_id:
                return jsonify({'Error': 'No se pudo obtener el id del chat'}), 500

            return jsonify({'chat_id': chat_id[0]}), 200
        
        return jsonify({'Error': 'No se pudo conectar a la base de datos'}), 500

    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    
@chatsBp.route('/user/chat/<id>', methods=['DELETE'])
@jwt_required()
def delete_chat_by_id(id):
    """
    Elimina un chat por su ID.

    Args:
        id (str): ID del chat.

    Returns:
        jsonify: True si se elimina correctamente, sino, un mensaje de error.
    """
    if not id:
        return jsonify({'Error':'No hay ningun id'})
    
    try:

        connection = PostgresConnectionBD()
        connection.connect()

        if connection.is_connected():
            print('Eliminando chat con id ', id)

            query = DELETE_CHAT(chat_id=id)
            connection.set_query_and_no_return(query)

            connection.disconnect()

            return jsonify(True)
        
        return jsonify({'Error': 'No se pudo conectar a la base de datos'}), 500
    
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
