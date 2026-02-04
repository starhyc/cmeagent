from typing import Dict, List

class ReportDataAggregator:
    def __init__(self):
        pass

    def aggregate_data(self, analysis_result: Dict, timeline: List[Dict], call_chain: List[Dict]) -> Dict:
        return {
            "overview": self._build_overview(analysis_result),
            "symptoms": self._extract_symptoms(analysis_result),
            "root_cause": analysis_result.get("root_cause", {}),
            "solutions": self._generate_solutions(analysis_result),
            "improvements": self._suggest_improvements(analysis_result),
            "timeline": timeline,
            "call_chain": call_chain,
            "confidence": analysis_result.get("overall_confidence", 0.5)
        }

    def _build_overview(self, analysis_result: Dict) -> str:
        summary = analysis_result.get("summary", "")
        confidence = analysis_result.get("overall_confidence", 0.5)
        return f"{summary} (Confidence: {confidence:.0%})"

    def _extract_symptoms(self, analysis_result: Dict) -> List[str]:
        issues = analysis_result.get("ranked_issues", [])
        return [f"{issue.get('severity', 'UNKNOWN')}: {issue.get('message', 'No message')}" for issue in issues[:5]]

    def _generate_solutions(self, analysis_result: Dict) -> List[str]:
        root_cause = analysis_result.get("root_cause", {})
        analysis_text = root_cause.get("analysis", "")
        return [analysis_text]

    def _suggest_improvements(self, analysis_result: Dict) -> List[str]:
        return ["Add monitoring for similar issues", "Improve error handling", "Add unit tests"]
