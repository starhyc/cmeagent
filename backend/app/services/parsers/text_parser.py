import re
from datetime import datetime
from typing import Dict, Optional

class PlainTextLogParser:
    def __init__(self):
        self.timestamp_patterns = [
            r'(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2})',
            r'(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})',
        ]
        self.level_pattern = r'\b(DEBUG|INFO|WARN|WARNING|ERROR|FATAL|EXCEPTION)\b'

    def parse_line(self, line: str) -> Optional[Dict]:
        timestamp = self._extract_timestamp(line)
        level = self._extract_level(line)

        return {
            "timestamp": timestamp,
            "level": level,
            "module": None,
            "message": line.strip(),
            "raw": line
        }

    def _extract_timestamp(self, line: str) -> Optional[datetime]:
        for pattern in self.timestamp_patterns:
            match = re.search(pattern, line)
            if match:
                try:
                    ts_str = match.group(1).replace('T', ' ')
                    return datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
                except:
                    pass
        return None

    def _extract_level(self, line: str) -> Optional[str]:
        match = re.search(self.level_pattern, line, re.IGNORECASE)
        return match.group(1).upper() if match else None
