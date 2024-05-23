import ollama
import json

class Utils:
    
    @staticmethod
    def ask_to_the_llama(message):
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': message,
            },
        ])
        
        return response
    @staticmethod
    def stream_from_the_llama(message):
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': message,
            },
        ],
        stream=True
        )
        for chunk in response:
            yield f"{json.dumps(chunk)}\n".encode('utf-8')
        return response