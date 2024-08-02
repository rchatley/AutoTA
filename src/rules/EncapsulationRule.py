import ast as python_ast

from src.filters.JavaFilter import JavaFilter
from src.rules.Rule import Rule


# Checks that all classes within scope are Encapsulated
class EncapsulationRule(Rule):
    def __init__(self, scope='project'):
        super().__init__(scope)

    def apply(self, file):
        ast = self.file_filter(file)
        if ast is None:
            return []

        feedback = []
        for ast_class in JavaFilter(node_class='class').get_nodes(ast):
            visible_fields = JavaFilter(node_class='field',
                                        node_modifiers=['private'],
                                        negatives=[
                                            'node_modifiers']).get_nodes(ast_class)

            for field in visible_fields:
                line, char = field.position
                feedback.append(
                    (line, f'The {field.declarators[0].name} '
                           f'field should be private'))

        return feedback

    def __str__(self):
        return f'-Encapsulation Rule'
