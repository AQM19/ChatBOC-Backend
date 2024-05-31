from src.api import db
import uuid

class ChatMessage(db.Model):
    
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.String(36), primary_key=True, unique=True, default=str(uuid.uuid4))
    chat_id = db.Column(db.String(36), db.ForeignKey('chats.id'), nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    message = db.Column(db.Text, nullable=True)
    is_response = db.Column(db.Boolean, nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    
    def __init__(self, chat_id=None, user_id=None, message=None, is_response=None):
        self.id = str(uuid.uuid4())
        self.chat_id = chat_id
        self.user_id = user_id
        self.message = message
        self.is_response = is_response