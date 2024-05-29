from src.services.chroma_connection import chromadb_connection
from utils.Utils import Utils

# l = []
# h = []
# for i in range(404001,404019):
#    l.append(Utils.transformpdf(f"src/scraper/docs/pdf_docs/{i}.pdf")) 

# for list in l:
#     for item in list:
#         h.append(item)

c = chromadb_connection()
# c.create_collection_from_documents("Otra",docs=h)
# c.add_documents_to_collection("Otra",docs=h)
r=c.query("BOC NÚM. 91","Otra")

print(r)
