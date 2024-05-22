import datetime

from classes.ollama_message import OllamaMessage

class OllamaResponse:
    
    def __init__(self, created_at: datetime, done: bool, done_reason: str, eval_count: int, eval_duration: int, load_duration: int, message: OllamaMessage, 
                 model: str, prompt_eval_count: int, prompt_eval_duration: int, total_duration: int):    
        self.created_at: datetime = created_at
        self.done: bool = done
        self.done_reason: str = done_reason
        self.eval_count: int = eval_count
        self.eval_duration: int = eval_duration
        self.load_duration: int = load_duration
        self.message: OllamaMessage = message
        self.model: str = model
        self.prompt_eval_count: int = prompt_eval_count
        self.prompt_eval_duration: int = prompt_eval_duration
        self.total_duration: int = total_duration