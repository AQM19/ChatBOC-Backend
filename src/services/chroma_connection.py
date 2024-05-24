from datetime import datetime
import os
import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma

import logging


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
        #Arrancamos logger
        self.logger = logging.getLogger(__name__)

        self.host = os.getenv("CHROMA_HOST")
        self.port = os.getenv("CHROMA_PORT")

        self.settings = Settings(
            anonymized_telemetry = False,
            allow_reset = True
        )

        self.client = None

        self.chroma_connection()

        #self.current_collection = None
        self.retriever = None
        self.embedding = None
        #self.splitter = RecursiveCharacterTextSplitter(chunk_size=2048, chunk_overlap=128)
    
 
    def chroma_connection(self):
        """
        Establece la conexión con el servidor ChromaDB utilizando la configuración proporcionada.
        """


        try:
            self.client = chromadb.HttpClient(host=self.host,port=self.port,settings=self.settings)
            self.logger.info(f"El servidor chroma está operativo. ")
            
        except ValueError:
            self.logger.error(f"Error al conectar al servidor de chroma. Compruebe que este arrancado. ")

    def create_collection(self, collection_name):
        """
        Crea una nueva colección en el servidor ChromaDB.

        Args:
            collection_name (str): Nombre de la colección a crear.
        """


        try:
            if self.__heartbeat():
                if not self.collection_exists(collection_name):

                    self.client.create_collection(collection_name)
                    self.logger.info(f"Coleccion {collection_name} creada correctamente")

        except ValueError:
            self.logger.error(f"No se pudo crear la colección {collection_name}. ",exc_info=1)

    def delete_collection(self, collection_name):
        """
        Elimina una colección existente en el servidor ChromaDB.

        Args:
            collection_name (str): Nombre de la colección a eliminar.
        """
        
        try:
            if self.__heartbeat():
                if  self.collection_exists(collection_name):
                    
                    self.client.delete_collection(collection_name)
                    self.logger.info(f"Coleccion {collection_name} borrada correctamente")

        except Exception:
            self.logger.error(f"No se pudo borrar la colección {collection_name}. Probablemente no exista.",exc_info=1)

    #TODO: este es el apartado de embeddings
    def insert_documents(self,docs,collection_name):        
        """
        Inserta documentos en una colección específica en el servidor ChromaDB.

        Args:
            docs (list): Documentos a insertar.
            collection_name (str): Nombre de la colección donde se insertarán los documentos.
        """
        try:
            if self.__heartbeat():
                if  self.collection_exists(collection_name):
                    
                    collection = self.client.get_or_create_collection(collection_name)
                    collection.add()

        except Exception:
            self.logger.error(f"No se pudo insertar el documento en {collection_name}.",exc_info=1)

    #TODO: este es el apartado de embeddings
    def query(self,query,collection_name,n_results):
        """
        Realiza una consulta en una colección específica en el servidor ChromaDB.

        Args:
            query (str): Texto de la consulta.
            collection_name (str): Nombre de la colección donde se realizará la consulta.
            n_results (int): Número de resultados a devolver.

        Returns:
            list: Resultados de la consulta.
        """
        
        try:
            if self.__heartbeat():
                if  self.collection_exists(collection_name):

                    collection = self.client.get_or_create_collection(collection_name)
                    results = collection.query(
                        query_texts=query, 
                        n_results=n_results
                    )

                    return results
        except ValueError:
            self.logger.error(f"Error al ejecutar la query.",exc_info=1)

    def reset_chroma(self):
        """Metodo de reset de chromadb. Borra toda la información de la base de datos
        """
    
        if self.__heartbeat():
            chroma_reboot = self.client.reset()
            self.logger.warn(f"ChromaDB se esta reiniciando...")

            if chroma_reboot:
                self.logger.warn(f"ChromaDB ha sido reiniciada.")

            else:
                self.logger.error(f"ChromaDB ha tenido problemas al reiniciarse.",exc_info=1)

        else:
            self.logger.warn(f"No se puedo conseguir el ultimo heartbeat de ChromaDB...")

    #region METODOS_PRIVADOS

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

        CHECK_LOGS_FOLDER = os.path.isdir(os.getenv("CHROMA_LOGS"))

        # Si la carpeta no existe la crea
        if not CHECK_LOGS_FOLDER:
            os.makedirs(os.getenv("CHROMA_LOGS"))

        #Fecha para organizar los logs
        date = datetime.now()
        format_date = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)


        #Arrancamos el logger
        logging.basicConfig(filename=f"{os.getenv('CHROMA_LOGS')}/chroma-{format_date}.log",
            level=logging.INFO,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def collection_exists(self,collection_name):
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

        self.logger.error(f"La coleccion {collection_name} no existe")
        return False
   
   
    #endregion