import os
from pathlib import Path
from typing import List, Dict
from app.services.code.tree_sitter_setup import tree_sitter_setup

class CodeScanner:
    def __init__(self):
        self.extensions = {
            'java': ['.java'],
            'python': ['.py'],
            'cpp': ['.cpp', '.cc', '.cxx', '.h', '.hpp'],
            'javascript': ['.js', '.jsx', '.ts', '.tsx']
        }

    def scan_directory(self, root_path: str) -> List[Dict]:
        files = []
        for ext_list in self.extensions.values():
            for ext in ext_list:
                files.extend(Path(root_path).rglob(f'*{ext}'))
        return [{'path': str(f), 'language': self._detect_language(f)} for f in files]

    def _detect_language(self, file_path: Path) -> str:
        ext = file_path.suffix
        for lang, exts in self.extensions.items():
            if ext in exts:
                return lang
        return 'unknown'

    def parse_file(self, file_path: str, language: str) -> Dict:
        parser = tree_sitter_setup.get_parser(language)
        if not parser:
            return None

        with open(file_path, 'rb') as f:
            content = f.read()

        tree = parser.parse(content)
        return {'path': file_path, 'tree': tree, 'content': content.decode('utf-8', errors='ignore')}
