import os
import javalang as java_ast


class JavaFile:

    def __init__(self, root, relative_path, file_name, contents=None):
        self.root = root
        self.relative_path = relative_path
        self.file_name = file_name
        self.feedback = []

        if contents is None:
            with open(os.path.join(root, file_name), 'r') as file:
                self.contents = file.read()
        else:
            self.contents = contents

        tokens = list(java_ast.tokenizer.tokenize(self.contents))
        self.ast = java_ast.parser.Parser(tokens).parse()
