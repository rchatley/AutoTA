import os

from javalang import tokenizer, tree
from javalang.parser import Parser

import ast as python_ast


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
            # self.public_nodes = self.get_public_nodes()
        else:
            self.ast = None

    def get_public_nodes(self):
        public_nodes = {}

        for path, node in self.ast:
            if isinstance(node, tree.InterfaceDeclaration):
                add_node_to_dict(public_nodes, node)
            elif hasattr(node, 'modifiers') and node.modifiers is not None:
                for modifier in node.modifiers:
                    if modifier == 'public':
                        add_node_to_dict(public_nodes, node)
                        break

        return public_nodes
