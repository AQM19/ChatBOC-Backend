from utils.Utils import Utils

class BaseService:
    def manage_response(question:str) -> str:
        response = Utils.ask_to_the_llama(message=question)
        
        # Mandar esto a una base de datos
        
        return response['message']['content']