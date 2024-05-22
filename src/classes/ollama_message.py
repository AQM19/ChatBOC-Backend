class OllamaMessage:
    
    def __init__(self, content: str, role: str):    
        self.content: str = content
        self.role: str = role