import datetime

from classes.OllamaMessage import OllamaMessage


class OllamaResponse:
    created_at: datetime
    done: bool
    done_reason: str
    eval_count: int
    eval_duration: int
    load_duration: int
    message: OllamaMessage
    model: str
    prompt_eval_count: int
    prompt_eval_duration: int
    total_duration: int