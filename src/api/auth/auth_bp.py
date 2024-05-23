from flask import Blueprint, jsonify, request, stream_with_context, Response
import bcrypt
from src.services.connection_db import ConnectionBD

authBp = Blueprint('auth', __name__)

@authBp.route('/login', methods=['GET'])
def login():
    data =request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    if not username or not email:
        return jsonify({'error': 'Username and password are required'}), 400
    
    salt = __user_exists(username, email)
    
    if not salt:
        return jsonify({'error': 'No se pudo encontrar al usuario'}), 400
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    connection = ConnectionBD()
    connection.connect()
        
        

@authBp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    try:
        __save_user_to_db(email, username, hashed_password, salt)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'User registered successfully'}), 201


def __save_user_to_db(email, username, hashed_password, salt):
    connection = ConnectionBD()
    
    connection.connect()
    
    if connection.is_connected():
        print('Registrando usuario...')
        
        rol_id = connection.select(
            'rols',
            ['id'],
            "rols.nemonic = 'User'"
        )
        
        connection.insert(
            'users',
            ['username', 'email', 'password_hash', 'salt', 'role_id'],
            [username, email, hashed_password, salt, rol_id]
        )
        
    connection.disconnect()
    
def __user_exists(username = None, email = None):
    
    if not username and not email:
        return jsonify({'error': 'Username and email are required'}), 400
    
    connection = ConnectionBD()
    connection.connect()
    
    if connection.is_connected():
        salt = None
        
        if username:
           salt = connection.select(
               'users',
               '[salt]',
               'users.username = %s', (username)
           )
           
        if email:
            salt = connection.select(
               'users',
               '[salt]',
               'users.email = %s', (email)
            )
        
    connection.disconnect()
    
    return salt