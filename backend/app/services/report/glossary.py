from openai import OpenAI
from app.core.config import settings
from typing import List

class GlossaryGenerator:
    def __init__(self):
        self.client = OpenAI(base_url=settings.LLM_ENDPOINT, api_key=settings.LLM_API_KEY)

    def generate_glossary(self, report_content: str) -> str:
        prompt = f"""Extract technical terms from the following report and provide brief definitions:

{report_content[:2000]}

Return a glossary in this format:
- **Term**: Definition
"""

        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
