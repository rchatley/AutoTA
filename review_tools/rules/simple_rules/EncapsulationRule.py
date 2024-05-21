from review_tools.rules.simple_rules.SimpleRule import SimpleRule
from review_tools.filters.JavaFilter import JavaFilter


class EncapsulationRule(SimpleRule):
    def __init__(self, scope='project'):
        super().__init__(scope)
        self.traversal = self.build_traversal()
        self.rule = self.build_rule()

    def build_traversal(self):
        def traversal(ast):
            unencapsulated_fields = []

            classes = JavaFilter(node_class='class').get_nodes(ast)
            for ast_class in classes:
                class_fields = JavaFilter(node_class='field').get_nodes(
                    ast_class)
                encapsulated_fields = JavaFilter(
                    node_class='field',
                    node_modifiers=[
                        'private', 'final']).get_nodes(ast_class)
                unencapsulated_fields.extend(
                    [field for field in class_fields if
                     field not in encapsulated_fields])

            return unencapsulated_fields

        return traversal
