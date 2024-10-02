import os

import javalang as java_ast
from javalang.tree import CompilationUnit

from src.project.Feedback import LineFeedback


class JavaFile:

    ast: CompilationUnit
    feedback: list[LineFeedback]

    def __init__(self, root, file_path: str, contents=None):
        self.root = root
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.relative_path = os.path.relpath(file_path, root)
        self.contents = contents
        self.feedback = []
        self.gpt_feedback = None
        self.ast = self._parse_file()

    def _parse_file(self):
        if self.contents is None:
            with open(os.path.join(self.root, self.file_path), 'r') as file:
                self.contents = file.read()

                tokens = list(java_ast.tokenizer.tokenize(self.contents))
                return java_ast.parser.Parser(tokens).parse()

    def full_file_path(self) -> str:
        return os.path.join(self.relative_path, self.file_name)

    def package_name(self) -> str:
        return self.ast.package.name if hasattr(self.ast, 'package') else None

    def contents_with_line_numbers(self):
        lines = self.contents.split('\n')
        return '\n'.join([f'{i + 1}: {line}' for i, line in enumerate(lines)])

