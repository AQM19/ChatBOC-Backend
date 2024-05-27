from typing import Any
from langchain_community.embeddings import OllamaEmbeddings


class CustomEmbeddingOllama:
    def __init__(self,model) -> None:
        self.embedding_model = OllamaEmbeddings(model=model)

    def __call__(self, input) -> Any:
        return self.embedding_model._embed(input)