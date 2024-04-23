import os
import re

from javalang import tree


def stock_traversal():
    return ""


node_dict = {'node': tree.Declaration, 'method': tree.MethodDeclaration, 'class': tree.ClassDeclaration,
             'field': tree.FieldDeclaration, 'constructor': tree.ConstructorDeclaration}


class TraversalRule:
    # rule_type = {'identifier', 'encapsulation', 'style', 'duplication', 'pattern'}

    # Identifier
    # WITHIN A SINGLE DIRECTORY/FILE/CLASS (or entire project)
    # NODE TYPE
    # ANNOTATION
    # EVERY / ATLEAST ONE
    # MUST/NOT
    # Follow some regex rule {pattern:}

    # Encapsulation
    # WITHIN A SINGLE DIRECTORY/FILE/CLASS (or entire project)
    # NODE TYPE
    # ANNOTATION
    # EVERY / ATLEAST ONE
    # MUST/NOT
    # Follow encapulsation {modifiers: private, final}

    # Design Pattern

    # NO AST===================================
    # Style
    # WITHIN A SINGLE DIRECTORY/FILE/CLASS (or entire project)
    # NODE TYPE
    # ANNOTATION
    # EVERY / ATLEAST ONE
    # MUST/NOT
    # Follow style

    # Duplication
    # WITHIN A SINGLE DIRECTORY/FILE/CLASS (or entire project)
    # NODE TYPE
    # ANNOTATION
    # EVERY / ATLEAST ONE
    # MUST/NOT
    # Follow style

    def __init__(self, rule_type, node_type='node', quantifier='every', scope='project', modifier=True,
                 metadata=None):

        self.node_type = node_type
        self.quantifier = quantifier
        self.scope = scope
        self.modifier = modifier

        if rule_type != '':
            self.rule_type = rule_type
            self.metadata = metadata
            self.traversal_function = self.build_traversal()
        else:
            self.traversal_function = stock_traversal

    def __str__(self):
        modifier_string = 'must' if self.modifier else 'must not'
        prefix = self.quantifier.capitalize() if self.scope == 'project' else f'In {self.scope[0]} {self.scope[1]}, {self.quantifier}'

        if self.rule_type == 'identifier':
            return f'{prefix} {self.node_type} {modifier_string} have an identifier of the format ' + self.metadata[
                'pattern']

    def build_traversal(self):
        tree_subset = node_dict[self.node_type]

        if self.rule_type == 'identifier':
            pattern = self.metadata['pattern']

            def rule(review_file):
                ast = review_file.ast
                return [f"({node.position[0]}, {node.position[1]}) | {self}"
                        for path, node in ast.filter(tree_subset) if re.match(pattern, node.name)]

        elif self.rule_type == 'encapsulation':
            def rule(review_file):
                ast = review_file.ast

                fields = [node for path, node in ast.filter(tree.ClassDeclaration)
                          if node is tree.FieldDeclaration]

                print(fields)

                return [f"({node.position[0]}, {node.position[1]}) | {self}"
                        for path, node in ast.filter(tree_subset) if False]

        else:
            rule = stock_traversal

        def traversal(review_file):
            if not self.filter_nodes(review_file):
                return []
            return rule(review_file)

        return traversal

    def filter_nodes(self, review_file):
        if self.scope == 'project':
            return True

        root, filename = review_file.root, review_file.file_name

        scope_type, scope = self.scope
        if scope_type == 'dir':
            directory_path = os.path.normpath(scope)
            return os.path.commonpath([os.path.normpath(root), directory_path]) == directory_path

        if scope_type == 'file':
            return filename == scope
