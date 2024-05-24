from src.services.connection_db import ConnectionBD
from utils.Utils import Utils
import json
from datetime import datetime

class ModelService:
    
    def __init__(self):
        self.connection = ConnectionBD()
    
    def manage_response(self, question) -> str:
        response = Utils.ask_to_the_llama(message=question)
        
        # Mandar esto a una base de datos
        model: str = response['model']
        created_at: str = response['created_at']
        done_reason: str = response['done_reason']
        done: bool = response['done']
        total_duration: int = response['total_duration']
        load_duration: int = response['load_duration']
        prompt_eval_duration: int = response['prompt_eval_duration']
        eval_count: int = response['eval_count']
        eval_duration: int = response['eval_duration']
        
        self.connection.connect()
        
        if self.connection.is_connected():
            print('Insertando datos...')
            # Discutir el flujo de información para obtener el id del chat.
                   
            self.connection.insert(
                'model_runs',
                ['user_id', 'created_at', 'done', 'done_reason', 'eval_count', 'eval_duration', 'load_duration', 'model', 'prompt_eval_duration', 'total_duration'], 
                ['39da072c-69ab-4f1b-abb3-1feb6b586ec1', created_at, done, done_reason, eval_count, eval_duration, load_duration, model, prompt_eval_duration, total_duration]
            )
            
            self.connection.disconnect()
            
        
        message = response['message']
        
        return response['message']['content']