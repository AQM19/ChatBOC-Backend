import ollama
import markdown
from utils.driverDB import DB
user_id = "2f86408f-e2f5-45f7-b9df-58c65f7ce252"
chat_id = "039acaf2-8c29-4857-a194-7d68de5a4052"
while(True):
  question = input("\nTu pregunta: ")
  response = ""
  chunks = []
  if question == "/exit":
    print("Hasta pronto!")
    break
  stream = ollama.chat(
      model='llama3',
      messages=[{'role': 'user', 'content': question}],
      stream=True,
  )
  print("Respondiendo a tu pregunta: ", question)
  db = DB(user_id)
  #chat_id = db.getChatID(db.getUserID())
  #db.getStream(stream, chat_id)

  for chunk in stream:
    # print(chunk)
    print(chunk['message']['content'], end='', flush=True)
    response += chunk['message']['content']
    chunks.append(chunk)
  response_html = markdown.markdown(response)
  print(response_html)
  db.saveChunks(chat_id, user_id, chunks)
  