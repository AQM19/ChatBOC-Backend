import ollama

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