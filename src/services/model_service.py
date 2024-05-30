from src.services.postgres_connection_db import PostgresConnectionBD
from utils.Utils import Utils
from flask import session

class ModelService:
    
    def __init__(self):
        self.connection = PostgresConnectionBD()
    
    def manage_response(self, question) -> str:

        response = Utils.ask_to_the_llama(question)
        
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

            user_id = session.get('user_id')
            
            self.connection.insert_with_no_result(
                'model_runs',
                ['user_id', 'created_at', 'done', 'done_reason', 'eval_count', 'eval_duration', 'load_duration', 'model', 'prompt_eval_duration', 'total_duration'], 
                [str(user_id), created_at, done, done_reason, eval_count, eval_duration, load_duration, model, prompt_eval_duration, total_duration]
            )
            
            self.connection.disconnect()
        
        return response['message']['content']