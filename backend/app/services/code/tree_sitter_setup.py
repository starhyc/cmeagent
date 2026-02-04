from tree_sitter import Language, Parser
import os

class TreeSitterSetup:
    def __init__(self):
        self.languages = {}
        self.parsers = {}

    def setup_language(self, lang_name: str, so_path: str):
        language = Language(so_path, lang_name)
        parser = Parser()
        parser.set_language(language)
        self.languages[lang_name] = language
        self.parsers[lang_name] = parser
        return parser

    def get_parser(self, lang_name: str):
        return self.parsers.get(lang_name)

tree_sitter_setup = TreeSitterSetup()
