from openai import OpenAI
from app.core.config import settings
from typing import List, Dict

class RootCauseAnalyzer:
    def __init__(self):
        self.client = OpenAI(base_url=settings.LLM_ENDPOINT, api_key=settings.LLM_API_KEY)

    def analyze_root_cause(self, error_logs: List[Dict], call_chain: List[Dict], code_context: str = None) -> Dict:
        prompt = self._build_analysis_prompt(error_logs, call_chain, code_context)

        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "analysis": response.choices[0].message.content,
            "confidence": "high"
        }

    def _build_analysis_prompt(self, error_logs: List[Dict], call_chain: List[Dict], code_context: str) -> str:
        prompt = """Analyze the following error logs and call chain to identify the root cause:

## Error Logs:
"""
        for log in error_logs[:5]:
            prompt += f"- [{log.get('level')}] {log.get('timestamp')}: {log.get('message')}\n"

        prompt += "\n## Call Chain:\n"
        for call in call_chain[:10]:
            prompt += f"- {call.get('module')}: {call.get('message')}\n"

        if code_context:
            prompt += f"\n## Code Context:\n{code_context}\n"

        prompt += """
Provide:
1. Root cause of the issue
2. Which module/component is responsible
3. Why the error occurred
4. Recommended fix"""

        return prompt
