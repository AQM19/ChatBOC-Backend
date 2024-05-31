from datetime import datetime
from dotenv import load_dotenv
import logging
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.classes.Scrapper import Scrapper


def main():
    load_dotenv()
    logs_path: str = os.getenv('LOGS_PATH')

    # Comprobamos si la carpeta de logs esta creada
    check_logs_folder: bool = os.path.isdir(logs_path)

    # Si la carpeta no existe la crea
    if not check_logs_folder:
        os.makedirs(logs_path)

    # Fecha para organizar los logs
    date: datetime = datetime.now()
    format_date: str = str(date.year) + str(date.month).zfill(2) + \
        str(date.day).zfill(2)

    # Arrancamos el logger
    logging.basicConfig(filename=f"{logs_path}/scraper-{format_date}.log", level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    s: Scrapper = Scrapper()
    s.scrape_All_PDFs()


if __name__ == '__main__':
    main()
