import os
import ast as python_ast
import javalang as java_ast


class ReviewFile:

    def __init__(self, root, file_name, contents=None):
        self.root = root
        self.file_name = file_name

        if contents is None:
            with open(os.path.join(root, file_name), 'r') as file:
                self.contents = file.read()
        else:
            self.contents = contents

        extension = os.path.splitext(file_name)[1]

        if extension == '.py':
            self.language = 'python'
            self.ast = python_ast.parse(self.contents)
        elif extension == '.java':
            self.language = 'java'
            tokens = list(java_ast.tokenizer.tokenize(self.contents))
            self.ast = java_ast.parser.Parser(tokens).parse()
        else:
            self.ast = None
