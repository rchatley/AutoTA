from review.filters.JavaFilter import JavaFilter
from review.rules.Rule import Rule


# Checks that all classes within scope are Encapsulated
class EncapsulationRule(Rule):
    def __init__(self, scope='project', getters=False, setters=False):
        super().__init__(scope)
        self._getters = getters
        self._setters = setters

    def apply(self, file):
        ast = self.filter(file)
        if file is None:
            return []

        feedback = []
        for ast_class in JavaFilter(node_class='class').get_nodes(ast):
            visible_fields = JavaFilter(node_class='field',
                                        node_modifiers=['private'],
                                        negatives=[
                                            'node_modifiers']).get_nodes(
                ast_class)

            for field in visible_fields:
                line, char = field.position
                feedback.append(
                    f'{file.file_name}:{line}:{char}: In class {ast_class.name}, '
                    f'the {field.declarators[0].name} field is '
                    f'not private')

            if self._getters:
                pass

            if self._setters:
                pass

        return feedback
