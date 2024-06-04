from src.api import db
import uuid

class ModelRun(db.Model):
    
    __tablename__ = 'model_runs'
    
    id = db.Column(db.String(36), primary_key=True, unique=True, default=str(uuid.uuid4))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
    done = db.Column(db.Boolean, nullable=True)
    done_reason = db.Column(db.String(100), nullable=True)
    eval_count = db.Column(db.BigInteger, nullable=True)
    eval_duration = db.Column(db.BigInteger, nullable=True)
    load_duration = db.Column(db.BigInteger, nullable=True)
    model = db.Column(db.String(50), nullable=True)
    prompt_eval_duration = db.Column(db.BigInteger, nullable=True)
    total_duration = db.Column(db.BigInteger, nullable=True)
    
    def __init__(self, user_id=None, done=None, done_reason=None, eval_count=None, eval_duration=None, load_duration=None, model=None, prompt_eval_duration=None, total_duration=None):
        self.id = str(uuid.uuid4())  # Genera un UUID aleatorio
        self.user_id = user_id
        self.done = done
        self.done_reason = done_reason
        self.eval_count = eval_count
        self.eval_duration = eval_duration
        self.load_duration = load_duration
        self.model = model
        self.prompt_eval_duration = prompt_eval_duration
        self.total_duration = total_duration