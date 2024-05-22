from review_tools.filters.JavaFilter import JavaFilter
from review_tools.rules.simple_rules.SimpleRule import SimpleRule


class IdentifierRule(SimpleRule):
    def __init__(self, scope='project', node_class='node', node_name='.*',
                 annotations=None):
        super().__init__(scope)
        self.node_name = node_name
        self.node_class = node_class

        self.traversal = self.build_traversal()
        self.rule = self.build_rule()
        self.annotations = annotations

    def build_traversal(self):
        def traversal(ast):
            return JavaFilter(node_class=self.node_class,
                              node_name=self.node_name).get_nodes(
                ast)

        return traversal
