import ast as python_ast

from src.filters.JavaFilter import JavaFilter
from src.project.Feedback import LineFeedback
from src.rules.Rule import Rule


class ClassExtendingSuperclassCheck(Rule):
    def __init__(self, scope='project', superclass_type=None):
        super().__init__(scope)
        self.superclass_type = superclass_type

    def apply(self, file) -> list[LineFeedback]:
        ast = self.file_filter(file)
        if ast is None:
            return []

        feedback: list[LineFeedback] = []
        for ast_class in JavaFilter(node_class='class', node_extends=self.superclass_type).get_nodes(ast):
            print("found " + ast_class.name)
            line, char = ast_class.position
            feedback.append(
                LineFeedback(line_number=line,
                             feedback=f'The class {ast_class.name} should not extend {self.superclass_type}.'))

        return feedback

    def __str__(self):
        return f'-Access Modifier Check'
