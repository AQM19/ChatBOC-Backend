"""-------PROXIES WEB AGENTS-------"""

PROXIES_URL="https://geonode.com/free-proxy-list"
PROXIES_API_SELECT_PAGE="https://proxylist.geonode.com/api/proxy-list?limit=500&page="
PROXIES_API_END="&sort_by=lastChecked&sort_type=desc"
PROXIE_TEST_URL="https://httpbin.org/ip"
PAGE_NUMBER=4 #Each page has 500 proxies, defaults to 1. If needed, max is 9.
PROXIES_FILENAME="Scraper/Proxies.csv"

WEB_AGENTS="Business\\user-agents.txt"

"""--------------------------------"""

BOC="https://boc.cantabria.es/boces/verAnuncioAction.do?idAnuBlob="
DOCS_PATH="src/scraper/docs"
PDFS_PATH=f"{DOCS_PATH}/pdf_docs"


PATIENCE = 20

# Este es el número de iteraciones de prueba de urls máximo que hará el scraper. Es un parámetro que hasta que no se superen ese millón de documentos subidos al BOC no hará falta tocarlo.
NUM_ITER_MAX=100000
FIRST_DOWNLOAD=403000 #El BOC ya sabemos que tiene más de 400000 pdfs
NUM_PROCESSES = 20

LOGS_PATH="C:/Users/danib/Desktop/Chat-BOC/src/scraper/logs/"

#ChromaDB
CHROMA_SERVER_HOST='localhost'
CHROMA_SERVER_HTTP_PORT=8000