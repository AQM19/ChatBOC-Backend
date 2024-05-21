import ollama
import markdown

while(True):
  question = input("\nTu pregunta: ")
  response = ""
  if question == "/exit":
    print("Hasta pronto!")
    break
  stream = ollama.chat(
      model='llama3',
      messages=[{'role': 'user', 'content': question}],
      stream=True,
  )
  print("Respondiendo a tu pregunta: ", question)
  for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
    response += chunk['message']['content']
  response_html = markdown.markdown(response)
  print(response_html)