from typing import List, Dict
import re

class PerformanceAnomalyDetector:
    def __init__(self):
        self.timeout_patterns = [
            r'timeout',
            r'timed out',
            r'connection timeout',
            r'read timeout'
        ]
        self.slow_query_patterns = [
            r'slow query',
            r'query took (\d+)ms',
            r'execution time: (\d+)ms'
        ]

    def detect_anomalies(self, logs: List[Dict]) -> List[Dict]:
        anomalies = []

        for log in logs:
            message = (log.get('message') or '').lower()

            if self._is_timeout(message):
                anomalies.append({
                    'type': 'timeout',
                    'log': log,
                    'severity': 'high'
                })

            if self._is_slow_query(message):
                anomalies.append({
                    'type': 'slow_query',
                    'log': log,
                    'severity': 'medium'
                })

        return anomalies

    def _is_timeout(self, message: str) -> bool:
        return any(re.search(pattern, message, re.IGNORECASE) for pattern in self.timeout_patterns)

    def _is_slow_query(self, message: str) -> bool:
        return any(re.search(pattern, message, re.IGNORECASE) for pattern in self.slow_query_patterns)
