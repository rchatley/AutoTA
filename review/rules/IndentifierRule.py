from review.filters.JavaFilter import JavaFilter
from review.rules.Rule import Rule


class IdentifierRule(Rule):
    def __init__(self, scope='project', node_class='node', name_format='.*',
                 annotations=None):
        super().__init__(scope)
        self.node_name = name_format
        self.node_class = node_class
        self.annotations = annotations

        self.traversal = self.build_traversal()
        self.rule = self.build_rule()

    def build_traversal(self):
        def traversal(ast):
            return JavaFilter(node_class=self.node_class,
                              node_name=self.node_name,
                              node_annotations=self.annotations).get_nodes(
                ast)

        return traversal
