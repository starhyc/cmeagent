from app.services.parsers.json_parser import JSONLogParser
from app.services.parsers.text_parser import PlainTextLogParser
from app.services.parsers.keyvalue_parser import KeyValueLogParser
from typing import Dict, Optional

class LogNormalizer:
    def __init__(self):
        self.parsers = [
            JSONLogParser(),
            KeyValueLogParser(),
            PlainTextLogParser()
        ]

    def normalize(self, line: str) -> Optional[Dict]:
        for parser in self.parsers:
            result = parser.parse_line(line)
            if result and result.get("timestamp"):
                return result

        return self.parsers[-1].parse_line(line)
