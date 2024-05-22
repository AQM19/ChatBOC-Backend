import logging
from datetime import datetime
import os

from Business.Scraper import Scraper
import Business.Constants as Constants

def main ():

    #Comprobamos si la carpeta de logs esta creada
    CHECK_LOGS_FOLDER = os.path.isdir(Constants.LOGS_PATH)

    # Si la carpeta no existe la crea
    if not CHECK_LOGS_FOLDER:
        os.makedirs(Constants.LOGS_PATH)

    #Fecha para organizar los logs
    date = datetime.now()
    format_date = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)


    #Arrancamos el logger
    logging.basicConfig(filename=f"{Constants.LOGS_PATH}/scraper-{format_date}.log",level=logging.INFO,format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

    s = Scraper()
    s.scrape_All_PDFs()


if __name__=='__main__':
   main()