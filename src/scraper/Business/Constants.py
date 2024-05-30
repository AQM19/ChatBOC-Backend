BOC="https://boc.cantabria.es/boces/verAnuncioAction.do?idAnuBlob="
DOCS_PATH="src/scraper/docs"
PDFS_PATH=f"{DOCS_PATH}/pdf_docs"


PATIENCE = 65

# Este es el número de iteraciones de prueba de urls máximo que hará el scraper. Es un parámetro que hasta que no se superen ese millón de documentos subidos al BOC no hará falta tocarlo.
NUM_ITER_MAX=1000000
DOWNLOAD_FROM=404000 #El BOC ya sabemos que tiene más de 400000 pdfs
NUM_PROCESSES = 20

LOGS_PATH="C:/Users/danib/Desktop/Chat-BOC/src/scraper/logs/"
