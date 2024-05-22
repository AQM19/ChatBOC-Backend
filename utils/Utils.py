import ollama
from src.classes import OllamaMessage, OllamaResponse

class Utils:
    
    @staticmethod
    def ask_to_the_llama(message):
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': message,
            },
        ])
        
        ollama_response = OllamaResponse(
            created_at=response['created_at'],
            done=response['done'],
            done_reason=response['done_reason'],
            eval_count=response['eval_count'],
            eval_duration=response['eval_duration'],
            load_duration=response['load_duration'],
            message=OllamaMessage(**response['message']),
            model=response['model'],
            prompt_eval_count=response['prompt_eval_count'],
            prompt_eval_duration=response['prompt_eval_duration'],
            total_duration=response['total_duration']
        )
        
        return ollama_response