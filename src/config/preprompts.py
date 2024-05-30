# v.1
PRE_PROMPT_V1 = lambda question, context=None: """Pregunta: {question}\n\nContexto (responde solo sobre el contenido del texto entregado): {context}"""

# v.2
PRE_PROMPT_V2 = lambda question, context=None: """<|begin_of_text|><|start_header_id|>system<|end_header_id|>Eres una asistente para respuesta de preguntas.
            Usa el contexto proporcionado para contestar a la pregunta. Si no conoces la respuesta, di que no conoces la respuesta.
            Responde siempre en español y con 4 frases como mucho. <|eot_id|><|start_header_id|>user<|end_header_id|>
            Question: {question}
            Context: {context}
            Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""