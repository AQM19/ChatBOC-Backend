from utils.Utils import Utils

class BaseService:
    def manage_response(self, question) -> str:
        response = Utils.ask_to_the_llama(message=question)
        
        # Mandar esto a una base de datos
        print(response)
        
        return response['message']['content']