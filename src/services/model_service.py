from src.models.ModelRun import ModelRun
from src.services.postgres_connection_db import PostgresConnectionBD
from utils.Utils import Utils
from flask import session
from src.api import db

class ModelService:
    
    def __init__(self):
        self.connection = PostgresConnectionBD()
    
    def manage_response(self, question) -> str:

        response = Utils.ask_to_the_llama(question)
        
        model: str = response['model']
        done_reason: str = response['done_reason']
        done: bool = response['done']
        total_duration: int = response['total_duration']
        load_duration: int = response['load_duration']
        prompt_eval_duration: int = response['prompt_eval_duration']
        eval_count: int = response['eval_count']
        eval_duration: int = response['eval_duration']
        
        user_id: str = session.get('user_id')

        new_model_run: ModelRun = ModelRun(done=done,done_reason=done_reason,eval_count=eval_count,eval_duration=eval_duration,load_duration=load_duration,model=model,prompt_eval_duration=prompt_eval_duration,total_duration=total_duration,user_id=user_id)
        db.session.add(new_model_run)
        db.session.commit()
    
        return response['message']['content']