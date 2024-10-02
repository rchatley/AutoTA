from src.filters.JavaFilter import JavaFilter
from src.project.Feedback import LineFeedback
from src.rules.Rule import Rule


class AccessModifierCheck(Rule):
    def __init__(self, scope='project', field_type=None, expected_modifiers=[]):
        super().__init__(scope)
        self.expected_modifiers = expected_modifiers
        self.field_type = field_type

    def apply(self, file) -> list[LineFeedback]:
        ast = self.file_filter(file)
        if ast is None:
            return []

        feedback: list[LineFeedback] = []
        for ast_class in JavaFilter(node_class='class').get_nodes(ast):
            visible_fields = (JavaFilter(node_class='field',
                                         node_type=self.field_type,
                                         node_modifiers=self.expected_modifiers,
                                         negatives=['node_modifiers'])
                              .get_nodes(ast_class))

            for field in visible_fields:
                line, char = field.position
                feedback.append(
                    LineFeedback(line_number=line,
                                 feedback=f'Make the {field.declarators[0].name} field {" and ".join(self.expected_modifiers)}'))

        return feedback

    def __str__(self):
        return f'-Access Modifier Check'
