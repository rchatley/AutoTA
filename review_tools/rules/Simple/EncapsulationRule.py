from review_tools.rules.filters.JavaFilter import JavaFilter
from review_tools.rules.Simple.SimpleRule import SimpleRule


class EncapsulationRule(SimpleRule):
    def __init__(self, scope='project'):
        super().__init__(scope)
        self.traversal = self.build_traversal()
        self.rule = self.build_rule()

    def build_traversal(self):
        def traversal(ast):
            unencapsulated_fields = []

            classes = JavaFilter(node_class='class').get_instances_of(ast)
            for ast_class in classes:
                class_fields = JavaFilter(node_class='field').get_instances_of(
                    ast_class)
                encapsulated_fields = JavaFilter(
                    node_class='field',
                    node_modifiers=[
                        'private', 'final']).get_instances_of(ast_class)
                unencapsulated_fields.extend(
                    [field for field in class_fields if
                     field not in encapsulated_fields])

            return unencapsulated_fields

        return traversal
