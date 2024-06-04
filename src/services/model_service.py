from flask import session
from src.api import db
from src.classes.chroma_connection_db import ChromaConnectionDB
from src.classes.postgres_connection_db import PostgresConnectionBD
from src.models.ModelRun import ModelRun
from utils.Utils import Utils

class ModelService:
    
    def __init__(self):
        self.postgres_connection = PostgresConnectionBD()
        self.chroma_connection = ChromaConnectionDB()
    
    def manage_response(self, question) -> str:
        """
        Maneja la respuesta para una pregunta utilizando un modelo de IA y guarda la ejecución del modelo en la base de datos.

        Args:
            question (str): Pregunta que se realiza al modelo de IA.

        Returns:
            str: Respuesta del modelo de IA.
        """
        context = self.chroma_connection.query(question, 'BOC')
        response = Utils.ask_to_the_llama(question=question, context=context)
        
        model: str = response['model']
        done_reason: str = response['done_reason']
        done: bool = response['done']
        total_duration: int = response['total_duration']
        load_duration: int = response['load_duration']
        prompt_eval_duration: int = response['prompt_eval_duration']
        eval_count: int = response['eval_count']
        eval_duration: int = response['eval_duration']
        user_id: str = session.get('user_id')

        new_model_run: ModelRun = ModelRun(done=done,done_reason=done_reason,eval_count=eval_count,eval_duration=eval_duration,
                    load_duration=load_duration,model=model,prompt_eval_duration=prompt_eval_duration,total_duration=total_duration,user_id=user_id)
        db.session.add(new_model_run)
        db.session.commit()
    
        return response['message']['content']