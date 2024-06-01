import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.classes.chroma_connection_db import ChromaConnectionDB


def main():

    print('HOLA')

    collection_name = 'BOC'
    connection = ChromaConnectionDB()

    if connection.collection_exists(collection_name):
        print('Existe')
        return
    
    print('No existe')

if __name__ == '__main__':
    main()