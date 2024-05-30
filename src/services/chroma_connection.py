from datetime import datetime
import os
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

import logging

from src.services import Constants


class chromadb_connection:
    """
    Clase para manejar la conexión y las operaciones con un servidor ChromaDB.
    """

    def __init__(self):
        """
        Inicializa la clase chromadb_connection, configurando los logs,
        obteniendo las configuraciones del entorno y estableciendo la conexión
        con el servidor ChromaDB.
        """

        self.__init_logs()
        load_dotenv()
        
        # Arrancamos logger
        self.logger = logging.getLogger(__name__)

        self.host = os.getenv('CHROMA_HOST')
        self.port = os.getenv('CHROMA_PORT')
        self.settings = Settings(anonymized_telemetry=False, allow_reset=True)
        self.client = None

        self.embedding_langchain = OllamaEmbeddings(model="llama3")

        self.__chroma_connection()

    def __chroma_connection(self):
        """
        Establece la conexión con el servidor ChromaDB utilizando la configuración proporcionada.
        """
        try:
            self.client = chromadb.HttpClient(
                host=self.host, port=self.port, settings=self.settings)
            self.logger.info(f"El servidor chroma está operativo. ")

        except ValueError:
            self.logger.error(
                f"Error al conectar al servidor de chroma. Compruebe que este arrancado. ")

    # region DOCUMENTS & QUERY

    def create_collection_from_documents(self, collection_name, docs):
        """
        Crea de 0 y añade documentos a una colección  en el servidor ChromaDB.

        Args:
            collection_name (str): Nombre de la colección donde se realizará la consulta.
            docs (list[Document]): Lista de documentos.
        """

        try:
            if self.__heartbeat():
                if not self.collection_exists(collection_name):
                    Chroma.from_documents(documents=docs, collection_name=collection_name,
                                          embedding=self.embedding_langchain, client=self.client)
                    self.logger.info(
                        f"Se ha creado la coleccion: {collection_name}.")
                    self.logger.info(f"Documentos insertados: {len(docs)}.")

                else:
                    self.logger.info(
                        f"Esta intentando crear una coleccion que ya existe {collection_name}.")

        except ValueError:
            self.logger.error(
                f"No se pudieron insertar documentos {collection_name}.", exc_info=1)

    def add_documents_to_collection(self, collection_name, docs):
        """
        Añade documentos a una colección específica en el servidor ChromaDB.

        Args:
            collection_name (str): Nombre de la colección donde se realizará la consulta.
            docs (list[Document]): Lista de documentos.
        """
        try:
            if self.__heartbeat():
                if self.collection_exists(collection_name):

                    vectorbase = Chroma(collection_name=collection_name,
                                        embedding_function=self.embedding_langchain, client=self.client)
                    vectorbase.add_documents(docs)

                    self.logger.info(
                        f"Documentos insertados: {len(docs)} en {collection_name}.")

        except ValueError:
            self.logger.error(
                f"No se pudieron insertar documentos en {collection_name}.", exc_info=1)

    def query(self, query, collection_name):
        """
        Realiza una consulta en una colección específica en el servidor ChromaDB.

        Args:
            query (str): Texto de la consulta.
            collection_name (str): Nombre de la colección donde se realizará la consulta.

        Returns:
            list: Resultados de la consulta.
        """

        try:
            if self.__heartbeat():
                if self.collection_exists(collection_name):

                    vectorbase = Chroma(collection_name=collection_name,
                                        embedding_function=self.embedding_langchain, client=self.client)
                    retriever = vectorbase.as_retriever()
                    results = retriever.invoke(query)

                    self.logger.info(f"Query {query} realizada con exito.")
                    return self._combine_docs(results)

        except ValueError:
            self.logger.error(
                f"Error al ejecutar la query > {query}.", exc_info=1)

    # endregion

    # region RESET CHROMA

    def delete_all_collections(self):
        """Metodo de reset de chromadb. Borra toda la información de la base de datos
        """

        if self.__heartbeat():
            collections = self.client.list_collections()

            for collection in collections:
                self.client.delete_collection(collection.name)
                self.logger.warn(f"Coleccion {collection.name} eliminada.")

            self.logger.warn(f"Todas las colecciones eliminadas.")

            print()
        else:
            self.logger.warn(
                f"No se puedo conseguir el ultimo heartbeat de ChromaDB...")

    # endregion

    # region METODOS_PRIVADOS

    def __heartbeat(self):
        """
        Verifica si el servidor ChromaDB está disponible mediante un 'heartbeat'.

        Returns:
            bool: True si el servidor está disponible, False en caso contrario.
        """
        try:
            self.client.heartbeat()
            return True
        except Exception:
            return False

    def __init_logs(self):
        """
        Inicializa la configuración de logs, creando la carpeta de logs si no existe
        y configurando el formato y el archivo de logs.
        """

        CHECK_LOGS_FOLDER = os.path.isdir(Constants.CHROMA_LOGS)

        # Si la carpeta no existe la crea
        if not CHECK_LOGS_FOLDER:
            os.makedirs(Constants.CHROMA_LOGS)

        # Fecha para organizar los logs
        date = datetime.now()
        format_date = str(date.year) + \
            str(date.month).zfill(2) + str(date.day).zfill(2)

        # Arrancamos el logger
        logging.basicConfig(filename=f"{Constants.CHROMA_LOGS}/chroma-{format_date}.log",
                            level=logging.INFO,
                            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S'
                            )

    def collection_exists(self, collection_name):
        """
        Verifica si una colección específica existe en el servidor ChromaDB.

        Args:
            collection_name (str): Nombre de la colección a verificar.

        Returns:
            bool: True si la colección existe, False en caso contrario.
        """

        collections = self.client.list_collections()
        for collection in collections:

            if collection_name == collection.name:
                self.logger.info(f"La coleccion {collection_name} ya existe")
                return True

        self.logger.warn(f"La coleccion {collection_name} no existe")
        return False

    def _combine_docs(self, docs):
        """
        Combina los documentos en una sola cadena de texto.

        Args:
            docs (list): Una lista de documentos.

        Returns:
            str: La cadena de texto que contiene la combinación de los documentos.
        """
        combined_docs = ""
        for doc in docs:
            combined_docs += doc.page_content + "\n"
        return combined_docs.rstrip('\n')

    # endregion

# from utils.Utils import Utils
# #ejemplo de uso
# chromavector = chromadb_connection()

# CUANDO SON MUCHOS

# l = []
# h = []

# for i in range(404001,404019):
#    l.append(Utils.transformpdf(f"src/scraper/docs/pdf_docs/{i}.pdf"))

# for list in l:
#     for item in list:
#         h.append(item)

# paginas = Utils.transformpdf ('src/scraper/docs/pdf_docs/404002.pdf')
# Si hay que crear la coleccion
# chromavector.create_collection_from_documents("test1",paginas)

# Añadir documentos
# chromavector.add_documents_to_collection("test1",paginas)

# text = chromavector.query("aspirantes que han superado el proceso selectivo para el acceso","test1")

# print(text)
