import re
from typing import List, Dict, Optional

class StackTraceExtractor:
    def __init__(self):
        self.patterns = [
            r'at\s+[\w.$<>]+\(([^)]+):(\d+)\)',
            r'File "([^"]+)", line (\d+)',
            r'^\s+at\s+(.+):(\d+):(\d+)',
        ]

    def extract_stack_trace(self, log_message: str) -> Optional[Dict]:
        lines = log_message.split('\n')
        stack_frames = []

        for line in lines:
            for pattern in self.patterns:
                match = re.search(pattern, line)
                if match:
                    stack_frames.append({
                        'file': match.group(1),
                        'line': int(match.group(2)),
                        'raw': line.strip()
                    })
                    break

        if stack_frames:
            return {
                'frames': stack_frames,
                'top_frame': stack_frames[0] if stack_frames else None
            }
        return None
