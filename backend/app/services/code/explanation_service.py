from openai import OpenAI
from app.core.config import settings

class CodeExplanationService:
    def __init__(self):
        self.client = OpenAI(base_url=settings.LLM_ENDPOINT, api_key=settings.LLM_API_KEY)

    def explain_code(self, code: str, language: str) -> str:
        prompt = f"""Explain the following {language} code in clear, concise terms:

```{language}
{code}
```

Provide:
1. What the code does
2. Key logic and algorithms
3. Important dependencies or patterns"""

        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
