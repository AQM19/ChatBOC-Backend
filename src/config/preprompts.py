# v.1
PRE_PROMPT_V1 = lambda question, context=None: """Pregunta: {question}\n\nContexto (responde solo sobre el contenido del texto entregado): {context}"""

# v.2
PRE_PROMPT_V2 = lambda question, context=None: """<|begin_of_text|><|start_header_id|>system<|end_header_id|>Eres una asistente para respuesta de preguntas.
            Usa el contexto proporcionado para contestar a la pregunta. Si no conoces la respuesta, di que no conoces la respuesta.
            Responde siempre en español y con 4 frases como mucho. <|eot_id|><|start_header_id|>user<|end_header_id|>
            Question: {question}
            Context: {context}
            Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

# v.3
PRE_PROMPT_CONTEXT_V3 = lambda context=None: """Contexto (responde solo sobre el contenido del texto entregado): {context}"""

# v.4
PRE_PROMPT_CONTEXT_V4 = lambda query, context: """
    Pregunta: {query}
    Contexto: (Response solo utilizando la información del texto proporcionado): {context}
    
    Instrucciones:
        1. Response solo utilizando la información proporcionada en el contexto.
        2. No añadas información externa o inventada.
        3. La respuesta debe estar completamente en español.
"""

# v.5
PRE_PROMPT_CONTEXT_V5 = lambda context: """
    Contexto: (Response solo utilizando la información del texto proporcionado): {context}
    
    Instrucciones:
        1. Response solo utilizando la información proporcionada en el contexto.
        2. No añadas información externa o inventada.
        3. La respuesta debe estar completamente en español.
"""