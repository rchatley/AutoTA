from review_tools.rules.JavaFilter import get_instances_of
from review_tools.rules.Simple.SimpleRule import SimpleRule


class EncapsulationRule(SimpleRule):
    def __init__(self, scope='project'):
        super().__init__(scope)
        self.traversal = self.build_traversal()
        self.rule = self.build_rule()

    def build_traversal(self):
        def traversal(ast):
            unencapsulated_fields = []

            classes = get_instances_of(ast, node_class='class')
            for ast_class in classes:
                class_fields = get_instances_of(ast_class, node_class='field')
                encapsulated_fields = get_instances_of(ast_class, node_class='field',
                                                       node_modifiers=['private', 'final'])
                unencapsulated_fields.extend([field for field in class_fields if field not in encapsulated_fields])

            return unencapsulated_fields

        return traversal
