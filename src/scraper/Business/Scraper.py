from typing import Any, Literal
from urllib import response
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
import logging
import os
import requests


class Scraper:

    def __init__(self) -> None:
        load_dotenv()
        self.docsCheckpoint: list[int] = []
        self.boc: str = os.getenv('BOC')
        self.docs_path: str = os.getenv('DOCS_PATH')
        self.pdfs_path: str = os.getenv('PDFS_PATH')
        self.patience: int = int(os.getenv('PATIENCE'))
        self.num_iter_max: int = int(os.getenv('NUM_ITER_MAX'))
        self.download_from: int = int(os.getenv('DOWNLOAD_FROM'))
        self.num_processes: int = int(os.getenv('NUM_PROCESSES'))

        # Arrancamos logger
        self.logger: logging.Logger = logging.getLogger(__name__)

        self.init()

    def init(self):
        # Comprobamos si la carpeta de descarga esta creada
        check_folder: bool = os.path.isdir(self.docs_path)

        if not check_folder:
            os.makedirs(self.pdfs_path)
            self.logger.info(f"> Se ha creado la carpeta:  {self.pdfs_path} ")

        else:
            self.logger.info(f"> {self.pdfs_path} ya existe.")

        # Leemos cuantos pdfs hay en el directorio en caso de corte o problema
        if len(os.listdir(self.pdfs_path)) == 0:
            self.logger.warn("? - No se encontraron documentos descargados.")
            self.logger.warn("? - La descarga comenzará desde cero.")

        else:
            # Con esto recogemos el id de los pdfs que ya tenemos descargados
            self.logger.warn(
                "? - Se encontraron documentos ya descargados... ")
            for path in os.listdir(self.pdfs_path):
                if os.path.isfile(os.path.join(self.pdfs_path, path)):
                    self.docsCheckpoint.append(int(path.split(".")[0]))

    def scrape_All_PDFs(self):

        validUrls: list = []
        patience: int = 0

        for i in tqdm(range(self.download_from, self.num_iter_max)):

            if i not in self.docsCheckpoint:
                testUrl: (tuple[Any, Literal[False]]
                          | tuple[Any, Literal[True]]) = self.get_Valid_Urls(f"{self.boc}{i+1}")
                url: (tuple[Any, Literal[False]] |
                      tuple[Any, Literal[True]]) = testUrl[0]
                error: (tuple[Any, Literal[False]] |
                        tuple[Any, Literal[True]]) = testUrl[1]

                if not error:
                    validUrls.append(url)

                elif patience == self.patience:
                    self.logger.info("? Se supero la paciencia")
                    break

                else:
                    self.logger.warn(
                        f"? Se encontró un error en {url}. Probablemente no exista.")
                    patience += 1
                    self.logger.warn(f"? Paciencia {patience}/{self.patience}")

        self.logger.info("> Iniciando descarga del BOC...")

        pool: ThreadPool = ThreadPool(processes=self.num_processes)
        pool.map(self.download_PDF, validUrls)
        pool.close()
        pool.join()

    def get_Valid_Urls(self, url):

        try:
            # Aquí le estamos diciendo que pruebe desde el último documento recuperado
            # hasta el número maximo de iteraciones seleccionado en constantes.

            headers: str = ""
            proxy: str = ""

            self.logger.info(f"> Comprobando {url}")

            # Hacemos la llamada, comprobamos si existe la url y si hay pdf
            r: response = requests.get(
                f"{url}", headers=headers, proxies=proxy)

            soup: BeautifulSoup = BeautifulSoup(r.text, 'html.parser')

            # Solo por el status code no podemos saber si existen documentos, asi que tenemos que buscarlo y tenerlo en cuenta
            error = soup.find('div', id='errorDocumento')

            if r.status_code == 200 and error is None:
                self.logger.info(f"? - La url {url} es valida :). ")
                return url, False

            else:
                self.logger.warn(
                    f"? - La url {url} devolvió un status code de : {r.status_code}. Div element -> {error.text}")
                return url, True

        except Exception as e:
            self.logger.error(
                f"X - Se ha encontrado un error en la comprobación de la url {url}.")
            self.logger.error(
                f"? - La url {url} devolvió un status code de : {r.status_code}. ")
            return url, True

    def download_PDF(self, url):
        headers: str = ""
        proxy: str = ""

        r: response = requests.get(
            f"{url}", stream=True, headers=headers, proxies=proxy)

        # Recogemos el id del fichero
        id: Any = url.split("=")[1]
        pdfPath: str = f"{self.pdfs_path}/{id}"

        with open(f"{pdfPath}.pdf", 'wb') as f:
            f.write(r.content)

        self.logger.info(f"> Documento .pdf {id} descargado.")
