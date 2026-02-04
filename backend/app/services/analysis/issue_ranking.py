from typing import List, Dict

class IssueRankingService:
    def __init__(self):
        self.severity_weights = {
            'FATAL': 10,
            'ERROR': 7,
            'EXCEPTION': 7,
            'WARNING': 3,
            'INFO': 1
        }

    def rank_issues(self, issues: List[Dict]) -> List[Dict]:
        for issue in issues:
            issue['score'] = self._calculate_score(issue)

        return sorted(issues, key=lambda x: x['score'], reverse=True)

    def _calculate_score(self, issue: Dict) -> float:
        severity = issue.get('severity', 'INFO')
        probability = issue.get('probability', 0.5)
        frequency = issue.get('frequency', 1)

        severity_score = self.severity_weights.get(severity, 1)
        return severity_score * probability * frequency
