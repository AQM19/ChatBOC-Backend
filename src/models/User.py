from src.api import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, unique=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(20), default='User')
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    is_deleted = db.Column(db.Boolean, default=False)
    
    def __init__(self, username, email, password, role='User'):
        self.id = str(uuid.uuid4())  # Esto generará un UUID aleatorio
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)