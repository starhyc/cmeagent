from typing import List, Dict

class AnalysisResultAggregator:
    def __init__(self):
        pass

    def aggregate_results(self, root_cause: Dict, issues: List[Dict], anomalies: List[Dict], code_locations: List[Dict]) -> Dict:
        return {
            "root_cause": root_cause,
            "ranked_issues": issues,
            "performance_anomalies": anomalies,
            "recommended_code_locations": code_locations,
            "overall_confidence": self._calculate_confidence(root_cause, issues, anomalies),
            "summary": self._generate_summary(root_cause, issues, anomalies)
        }

    def _calculate_confidence(self, root_cause: Dict, issues: List[Dict], anomalies: List[Dict]) -> float:
        base_confidence = 0.5

        if root_cause.get("confidence") == "high":
            base_confidence += 0.3

        if len(issues) > 0:
            base_confidence += 0.1

        if len(anomalies) > 0:
            base_confidence += 0.1

        return min(base_confidence, 1.0)

    def _generate_summary(self, root_cause: Dict, issues: List[Dict], anomalies: List[Dict]) -> str:
        summary = f"Found {len(issues)} issues"
        if anomalies:
            summary += f" and {len(anomalies)} performance anomalies"
        return summary
