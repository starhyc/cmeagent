from typing import List, Dict

class CodeChunker:
    def __init__(self, max_chunk_size: int = 1000):
        self.max_chunk_size = max_chunk_size

    def chunk_code(self, content: str, file_path: str) -> List[Dict]:
        lines = content.split('\n')
        chunks = []
        current_chunk = []
        current_size = 0

        for i, line in enumerate(lines):
            line_size = len(line)
            if current_size + line_size > self.max_chunk_size and current_chunk:
                chunks.append({
                    'content': '\n'.join(current_chunk),
                    'file_path': file_path,
                    'start_line': i - len(current_chunk) + 1,
                    'end_line': i
                })
                current_chunk = []
                current_size = 0

            current_chunk.append(line)
            current_size += line_size

        if current_chunk:
            chunks.append({
                'content': '\n'.join(current_chunk),
                'file_path': file_path,
                'start_line': len(lines) - len(current_chunk) + 1,
                'end_line': len(lines)
            })

        return chunks
