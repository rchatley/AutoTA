import ast as python_ast

from src.filters.JavaFilter import JavaFilter
from src.project.Feedback import LineFeedback
from src.rules.Rule import Rule


class ClassImplementingInterfaceCheck(Rule):
    def __init__(self, scope='project', interface_type=None):
        super().__init__(scope)
        self.interface_type = [interface_type]

    def apply(self, file) -> list[LineFeedback]:
        ast = self.file_filter(file)
        if ast is None:
            return []

        feedback: list[LineFeedback] = []
        for ast_class in JavaFilter(node_class='class', node_implements=self.interface_type).get_nodes(ast):
            print("found " + ast_class.name)
            line, char = ast_class.position
            feedback.append(
                LineFeedback(line_number=line,
                             feedback=f'The class {ast_class.name} should not implement List. '
                             f'The behaviour we have in add() does not match the contract of a List.'))

        return feedback

    def __str__(self):
        return f'-Access Modifier Check'
