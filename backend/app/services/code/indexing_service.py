from openai import OpenAI
from app.core.config import settings
from app.services.code.scanner import CodeScanner
from app.services.code.chunker import CodeChunker
from app.services.code.index_db import CodeIndexDB
from typing import List

class CodeIndexingService:
    def __init__(self):
        self.client = OpenAI(base_url=settings.LLM_ENDPOINT, api_key=settings.LLM_API_KEY)
        self.scanner = CodeScanner()
        self.chunker = CodeChunker()
        self.index_db = CodeIndexDB()

    def index_codebase(self, root_path: str):
        files = self.scanner.scan_directory(root_path)

        for file_info in files:
            parsed = self.scanner.parse_file(file_info['path'], file_info['language'])
            if not parsed:
                continue

            chunks = self.chunker.chunk_code(parsed['content'], file_info['path'])
            embeddings = self._generate_embeddings([c['content'] for c in chunks])
            self.index_db.add_chunks(chunks, embeddings)

    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(input=texts, model=settings.LLM_MODEL)
        return [item.embedding for item in response.data]
