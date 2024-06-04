from src.api import db
import uuid

class Rol(db.Model):
    
    __tablename__ = 'rols'
    
    id = db.Column(db.String(36), primary_key=True, unique=True, default=str(uuid.uuid4))
    nemonic = db.Column(db.String(20), unique=True, nullable=False)
    
    def __init__(self, nemonic):
        self.id = str(uuid.uuid4())  # Genera un UUID aleatorio
        self.nemonic = nemonic