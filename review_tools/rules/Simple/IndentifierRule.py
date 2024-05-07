import re

from review_tools.rules.JavaFilter import get_instances_of
from review_tools.rules.Simple.SimpleRule import SimpleRule


class IdentifierRule(SimpleRule):
    def __init__(self, scope='project', node_class='node', node_name='.*',
                 node_annotations=None):
        super().__init__(scope)
        self.node_name = node_name
        self.node_class = node_class
        self.node_annotations = node_annotations

        self.traversal = self.build_traversal()
        self.rule = self.build_rule()

    def build_traversal(self):
        def traversal(ast):
            return get_instances_of(ast, node_class=self.node_class,
                                    node_name=self.node_name,
                                    node_annotations=self.node_annotations)

        return traversal
