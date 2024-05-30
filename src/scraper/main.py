import logging
from datetime import datetime
import os
from dotenv import load_dotenv
from Business.Scraper import Scraper


def main():
    load_dotenv()
    pdfs_path = os.getenv('PDFS_PATH')

    # Comprobamos si la carpeta de logs esta creada
    CHECK_LOGS_FOLDER = os.path.isdir(pdfs_path)

    # Si la carpeta no existe la crea
    if not CHECK_LOGS_FOLDER:
        os.makedirs(pdfs_path)

    # Fecha para organizar los logs
    date = datetime.now()
    format_date = str(date.year) + str(date.month).zfill(2) + \
        str(date.day).zfill(2)

    # Arrancamos el logger
    logging.basicConfig(filename=f"{pdfs_path}/scraper-{format_date}.log", level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    s = Scraper()
    s.scrape_All_PDFs()


if __name__ == '__main__':
    main()
