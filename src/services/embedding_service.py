import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.classes.chroma_connection_db import ChromaConnectionDB
from utils.Utils import Utils


def main():

    collection_name = 'BOC'
    connection = ChromaConnectionDB()

    print('Transformando las páginas del pdf...')
    start_time_transformpdf = time.time()
    paginas = []
    paginas.extend(Utils.transformpdf('src/admin/docs/404001.pdf'))
    paginas.extend(Utils.transformpdf('src/admin/docs/404002.pdf'))
    paginas.extend(Utils.transformpdf('src/admin/docs/404003.pdf'))
    paginas.extend(Utils.transformpdf('src/admin/docs/404004.pdf'))
    paginas.extend(Utils.transformpdf('src/admin/docs/404005.pdf'))
    paginas.extend(Utils.transformpdf('src/admin/docs/404006.pdf'))
    paginas.extend(Utils.transformpdf('src/admin/docs/404007.pdf'))
    paginas.extend(Utils.transformpdf('src/admin/docs/404008.pdf'))
    end_time_transformpdf = time.time()
    
    transform_time = end_time_transformpdf - start_time_transformpdf
    
    print('Páginas creadas')
    print()

    if not connection.collection_exists(collection_name):
        print('Creación de colección e insertando documentos en ella')
        start_time_collection = time.time()
        connection.create_collection_from_documents(collection_name,paginas)
        end_time_collection = time.time()

        collection_time = end_time_collection - start_time_collection

    print()
    print('Ejecutando query')
    start_time_query = time.time()
    text = connection.query("aspirantes que han superado el proceso selectivo para el acceso",collection_name)
    end_time_query = time.time()

    query_time = end_time_query - start_time_query

    print()
    print(text)
    print()
    print('Tiempos de ejecución:')
    print(f'Transformación de PDFs: {transform_time:.2f} segundos')
    print(f'Creación de colección: {collection_time:.2f} segundos')
    print(f'Query: {query_time:.2f} segundos')

    return


if __name__ == '__main__':
    main()