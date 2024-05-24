from flask import Blueprint, jsonify, session
from flask_jwt_extended import jwt_required
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
            
        return chats
        
    except Exception as e:
        return jsonify({'Error': str(e)}), 500