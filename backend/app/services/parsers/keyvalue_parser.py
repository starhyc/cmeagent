import re
from datetime import datetime
from typing import Dict, Optional

class KeyValueLogParser:
    def __init__(self):
        self.kv_pattern = r'(\w+)=([^\s]+|"[^"]*")'

    def parse_line(self, line: str) -> Optional[Dict]:
        matches = re.findall(self.kv_pattern, line)
        data = {k: v.strip('"') for k, v in matches}

        return {
            "timestamp": self._parse_timestamp(data.get("timestamp") or data.get("time")),
            "level": data.get("level") or data.get("severity"),
            "module": data.get("module") or data.get("service"),
            "message": data.get("message") or data.get("msg") or line.strip(),
            "raw": line
        }

    def _parse_timestamp(self, ts: Optional[str]) -> Optional[datetime]:
        if not ts:
            return None
        try:
            return datetime.fromisoformat(ts.replace('Z', '+00:00'))
        except:
            return None
