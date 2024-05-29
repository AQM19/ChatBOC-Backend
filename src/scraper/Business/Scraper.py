import multiprocessing
from multiprocessing.pool import ThreadPool
import logging
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import os
# from pypdf import PdfReader


import Business.Constants as Constants

class Scraper:

    def __init__(self) -> None:

        self.docsCheckpoint = []
        
        #Arrancamos logger
        self.logger = logging.getLogger(__name__)

        self.init()
    
    def init(self):

        

        #Comprobamos si la carpeta de descarga esta creada
        CHECK_FOLDER = os.path.isdir(Constants.DOCS_PATH)

        

        if not CHECK_FOLDER:
            os.makedirs(Constants.PDFS_PATH)
            self.logger.info(f"> Se ha creado la carpeta:  {Constants.PDFS_PATH} ")

        else:
            self.logger.info(f"> {Constants.PDFS_PATH} ya existe.")
        
        #Leemos cuantos pdfs hay en el directorio en caso de corte o problema 
        if len(os.listdir(Constants.PDFS_PATH)) == 0:
            self.logger.warn("? - No se encontraron documentos descargados.")
            self.logger.warn("? - La descarga comenzará desde cero.")

        else:
            #Con esto recogemos el id de los pdfs que ya tenemos descargados
            self.logger.warn("? - Se encontraron documentos ya descargados... ")
            for path in os.listdir(Constants.PDFS_PATH):
                if os.path.isfile(os.path.join(Constants.PDFS_PATH, path)):
                    self.docsCheckpoint.append(int(path.split(".")[0]))

    def scrape_All_PDFs(self):

        validUrls=[]
        patience = 0

        for i in tqdm(range(Constants.DOWNLOAD_FROM,Constants.NUM_ITER_MAX)):

                if i not in self.docsCheckpoint:
                    testUrl=self.get_Valid_Urls(f"{Constants.BOC}{i+1}")

                    url = testUrl[0]
                    error = testUrl[1]
                    
                    if not error:
                        validUrls.append(url)

                    elif patience == Constants.PATIENCE:
                        self.logger.info("? Se supero la paciencia")
                        break

                    else:
                        self.logger.warn(f"? Se encontró un error en {url}. Probablemente no exista.")
                        patience += 1
                        self.logger.warn(f"? Paciencia {patience}/{Constants.PATIENCE}")

        

        self.logger.info("> Iniciando descarga del BOC...")
        
        pool=ThreadPool(processes=Constants.NUM_PROCESSES)
        pool.map(self.download_PDF,validUrls)
        pool.close()
        pool.join()

    def get_Valid_Urls(self,url):

        try:
            #Aquí le estamos diciendo que pruebe desde el último documento recuperado
            #hasta el número maximo de iteraciones seleccionado en constantes.
            
            headers = ""
            proxy = ""


            self.logger.info(f"> Comprobando {url}")

            #Hacemos la llamada, comprobamos si existe la url y si hay pdf
            r = requests.get(f"{url}", headers=headers,proxies=proxy)

            soup = BeautifulSoup(r.text, 'html.parser')

            # Solo por el status code no podemos saber si existen documentos, asi que tenemos que buscarlo y tenerlo en cuenta
            error = soup.find('div', id='errorDocumento')

            if r.status_code == 200 and error is None:
                self.logger.info( f"? - La url {url} es valida :). ")
                return url,False
            
            else:
                self.logger.warn( f"? - La url {url} devolvió un status code de : {r.status_code}. Div element -> {error.text}")
                return url,True

        except Exception as e:
            self.logger.error(f"X - Se ha encontrado un error en la comprobación de la url {url}.")
            self.logger.error( f"? - La url {url} devolvió un status code de : {r.status_code}. ")
            return url,True

    def download_PDF (self,url):
    
        headers = ""
        proxy = ""

        r = requests.get(f"{url}", stream = True,headers=headers,proxies=proxy)

        #Recogemos el id del fichero
        id = url.split("=")[1]
        pdfPath = f"{Constants.PDFS_PATH}/{id}"

        with open(f"{pdfPath}.pdf", 'wb') as f:           
            f.write(r.content)
        
    
        self.logger.info(f"> Documento .pdf {id} descargado.")




