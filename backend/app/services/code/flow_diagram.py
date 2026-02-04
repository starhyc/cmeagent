from openai import OpenAI
from app.core.config import settings

class FlowDiagramGenerator:
    def __init__(self):
        self.client = OpenAI(base_url=settings.LLM_ENDPOINT, api_key=settings.LLM_API_KEY)

    def generate_flow_diagram(self, code: str, language: str) -> str:
        prompt = f"""Analyze the following {language} code and generate a Mermaid flowchart diagram showing the business logic flow:

```{language}
{code}
```

Return ONLY the Mermaid syntax (starting with ```mermaid), showing:
- Main execution flow
- Decision points
- Function calls
- Error handling paths"""

        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
