import chromadb
from app.core.config import settings
import os

class CodeIndexDB:
    def __init__(self):
        os.makedirs(settings.CODE_INDEX_PATH, exist_ok=True)
        self.client = chromadb.PersistentClient(path=settings.CODE_INDEX_PATH)
        self.collection = self.client.get_or_create_collection(
            name="code_embeddings",
            metadata={"description": "Code chunks with embeddings"}
        )

    def add_chunks(self, chunks: list, embeddings: list):
        ids = [f"{chunk['file_path']}:{chunk['start_line']}" for chunk in chunks]
        documents = [chunk['content'] for chunk in chunks]
        metadatas = [{'file_path': chunk['file_path'], 'start_line': chunk['start_line'], 'end_line': chunk['end_line']} for chunk in chunks]

        self.collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

    def search(self, query_embedding: list, n_results: int = 5):
        return self.collection.query(query_embeddings=[query_embedding], n_results=n_results)
