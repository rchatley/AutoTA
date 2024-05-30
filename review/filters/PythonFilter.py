import ast as python_ast

from review.filters.Filter import Filter


class PythonFilter(Filter):
    def __init__(self, node_class=None, node_name=None):
        super().__init__('python')
        self.node_class = node_class
        self.node_name = node_name

        self.class_map = {'class': python_ast.ClassDef}

    def _filter_node_class(self, node):
        return isinstance(node, self.class_map[self.node_class])

    def _filter_node_name(self, node):
        if self.node_name is None:
            return True
        return True

    def _passes_filter(self, node):
        return all([
            self._filter_node_class(node),
            self._filter_node_name(node)
        ])

    def get_nodes(self, ast):
        nodes = [node for _, node in ast if self._passes_filter(node)]
        return nodes
