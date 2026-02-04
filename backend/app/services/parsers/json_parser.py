import json
from datetime import datetime
from typing import Dict, Optional

class JSONLogParser:
    def parse_line(self, line: str) -> Optional[Dict]:
        try:
            data = json.loads(line)
            return {
                "timestamp": self._parse_timestamp(data.get("timestamp") or data.get("time")),
                "level": data.get("level") or data.get("severity"),
                "module": data.get("module") or data.get("service"),
                "message": data.get("message") or data.get("msg"),
                "raw": line
            }
        except json.JSONDecodeError:
            return None

    def _parse_timestamp(self, ts: str) -> Optional[datetime]:
        if not ts:
            return None
        try:
            return datetime.fromisoformat(ts.replace('Z', '+00:00'))
        except:
            return None
