from openai import OpenAI
from app.core.config import settings
from app.services.code.index_db import CodeIndexDB
from app.services.code.indexing_service import CodeIndexingService

class CodeLocationRecommender:
    def __init__(self):
        self.client = OpenAI(base_url=settings.LLM_ENDPOINT, api_key=settings.LLM_API_KEY)
        self.indexing_service = CodeIndexingService()
        self.index_db = CodeIndexDB()

    def recommend_locations(self, error_message: str, stack_trace: str = None) -> list:
        search_query = f"{error_message} {stack_trace or ''}"
        query_embedding = self.indexing_service._generate_embeddings([search_query])[0]
        results = self.index_db.search(query_embedding, n_results=5)

        recommendations = []
        for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
            recommendations.append({
                'file_path': meta['file_path'],
                'start_line': meta['start_line'],
                'end_line': meta['end_line'],
                'relevance_score': 1 - dist,
                'code_snippet': doc
            })

        return recommendations
