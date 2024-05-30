import ast as python_ast
import os

from javalang import tokenizer
from javalang.parser import Parser


def add_node_to_dict(node_dict, node):
    if node.name in node_dict:
        node_dict[node.name].append(node)
    else:
        node_dict[node.name] = [node]


class ReviewFile:

    def __init__(self, root, file_name):
        self.root = root
        self.file_name = file_name

        with open(os.path.join(root, file_name), 'r') as file:
            self.contents = file.read()

        extension = os.path.splitext(file_name)[1]

        if extension == '.py':
            self.ast = python_ast.parse(self.contents)
        elif extension == '.java':
            self.tokens = list(tokenizer.tokenize(self.contents))
            self.ast = Parser(self.tokens).parse()
        else:
            self.ast = None
