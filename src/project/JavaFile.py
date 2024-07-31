import os

import javalang as java_ast
from javalang.tree import CompilationUnit


class JavaFile:

    ast: CompilationUnit

    def __init__(self, root, file_path: str, contents=None):
        self.root = root
        self.file_name = file_path
        self.relative_path = os.path.relpath(file_path, root)
        self.contents = contents
        self.feedback = []
        self.ast = self._parse_file()

    def _parse_file(self):
        if self.contents is None:
            with open(os.path.join(self.root, self.file_name), 'r') as file:
                self.contents = file.read()

        tokens = list(java_ast.tokenizer.tokenize(self.contents))
        return java_ast.parser.Parser(tokens).parse()

    def full_file_path(self) -> str:
        return os.path.join(self.relative_path, self.file_name)

    def package_name(self) -> str:
        return self.ast.package.name if hasattr(self.ast, 'package') else None
