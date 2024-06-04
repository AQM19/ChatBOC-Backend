from src.api import db
import uuid

class Chat(db.Model):
    
    __tablename__ = 'chats'
    
    id = db.Column(db.String(36), primary_key=True, unique=True, default=str(uuid.uuid4))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(30), unique=True, nullable=True)
    
    def __init__(self, user_id=None, name=None):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.name = name