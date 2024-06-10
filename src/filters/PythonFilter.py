import ast
import ast as python_ast
import re

from src.filters.Filter import Filter


class SpecificNodeVisitor(python_ast.NodeVisitor):
    def __init__(self, node_class=None, node_name=None, node_privacy=None):
        self.node_class = node_class
        self.node_name = node_name
        self.node_privacy = node_privacy
        self.class_map = {'class': python_ast.ClassDef,
                          'method': python_ast.FunctionDef,
                          'field': python_ast.Assign}
        self.nodes = []

    def _filter_node_class(self, node):
        return isinstance(node, self.class_map[self.node_class])

    def _filter_node_name(self, node):
        if self.node_name is None:
            return True
        if not hasattr(node, 'name'):
            return True
        return re.match(self.node_name, node.name)

    def _filter_node_privacy(self, node):
        if self.node_privacy is None:
            return True
        print('HERE')
        if isinstance(node, ast.Assign):

            for target in node.targets:

                if isinstance(target, ast.Name):

                    return not target.attr.startswith(
                        '_') if self.node_privacy else node.name.startswith(
                        '_')
        else:
            return True

    def _passes_filter(self, node):
        return all([
            self._filter_node_class(node),
            self._filter_node_name(node)
        ])

    def generic_visit(self, node):
        if self._passes_filter(node):
            self.nodes.append(node)
        super().generic_visit(node)


class PythonFilter(Filter):
    def __init__(self, node_class=None, node_name=None, node_privacy=None):
        super().__init__('python')
        self.node_class = node_class
        self.node_name = node_name
        self.node_privacy = node_privacy

    def get_nodes(self, ast):
        visitor = SpecificNodeVisitor(self.node_class, self.node_name,
                                      self.node_privacy)
        visitor.visit(ast)
        return visitor.nodes
