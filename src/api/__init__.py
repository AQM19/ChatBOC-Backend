from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
from flask_jwt_extended import JWTManager

load_dotenv()
db = SQLAlchemy()
jwt = JWTManager()

def deploy_api():
    api = Flask(__name__)
    
    api.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Cambia la URI de la base de datos según tus necesidades
    api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva el seguimiento de modificaciones para mejorar el rendimiento
    api.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    api.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Crea el objeto db
    db.init_app(api)
    jwt.init_app(api)

    with api.app_context():
        
        from .auth import authBp
        from .ollama import ollamaBp
        from .chats import chatsBp
        
        api.register_blueprint(authBp)
        api.register_blueprint(chatsBp)
        api.register_blueprint(ollamaBp)

    return api
