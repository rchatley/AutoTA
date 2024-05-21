import ast as python_ast


class PythonFilter:
    def __init__(self, node_class=None, node_name=None):
        self.node_class = node_class
        self.node_name = node_name

        self.class_map = {'class': python_ast.ClassDef}

    def filter_node_class(self, node):
        return isinstance(node, self.class_map[self.node_class])

    def filter_node_name(self, node):
        if self.node_name is None:
            return True
        return True

    def passes_filter(self, node):
        return all([
            self.filter_node_class(node),
            self.filter_node_name(node)
        ])

    def get_nodes_in(self, ast):
        nodes = [node for _, node in ast if self.passes_filter(node)]
        return nodes
