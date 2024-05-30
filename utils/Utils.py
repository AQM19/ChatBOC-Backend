import ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter


class Utils:

    @staticmethod
    def ask_to_the_llama(message):

        pre_prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>Eres una asistente para respuesta de preguntas.
            Usa el contexto proporcionado para contestar a la pregunta. Si no conoces la respuesta, di que no conoces la respuesta.
            Responde siempre en español y con 4 frases como mucho. <|eot_id|><|start_header_id|>user<|end_header_id|>
            Question: {question}
            Context: {context}
            Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': message,
            },
        ])

        return response

    @staticmethod
    def transformpdf(path, chunk_size=1024, chunk_overlap=128):
        """
        Transforma un archivo PDF en fragmentos de texto.

        Args:
            path (str): La ruta al archivo PDF.
            chunk_size (int, opcional): El tamaño de cada fragmento de texto. Por defecto es 1024.
            chunk_overlap (int, opcional): La superposición entre los fragmentos de texto. Por defecto es 128.

        Returns:
            tuple: Una lista de fragmentos de texto obtenidos del PDF y sus ids. 
        """

        data = PyPDFLoader(path)
        text_splitter = CharacterTextSplitter(
            separator='\n', length_function=len, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        splits = text_splitter.split_documents(data.load())

        return splits
