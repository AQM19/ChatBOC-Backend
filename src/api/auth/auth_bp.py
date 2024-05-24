from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash
from src.models.User import User
from src.api import db
from flask_jwt_extended import create_access_token

authBp = Blueprint('auth', __name__)

# Ruta para iniciar sesión y generar token JWT
@authBp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    # Set session data
    session['user_id'] = user.id
    session['user_name'] = user.username
    session['user_rol'] = user.role
    
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)

@authBp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Verifica si el usuario ya existe
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'Username or email already exists'}), 400

    # Crea un nuevo usuario
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201