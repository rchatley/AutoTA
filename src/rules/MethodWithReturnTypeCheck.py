import ast as python_ast

from src.filters.JavaFilter import JavaFilter
from src.rules.Rule import Rule


class MethodWithReturnTypeCheck(Rule):
    def __init__(self, scope='project', return_type=None, expected_modifiers=[]):
        super().__init__(scope)
        self.expected_modifiers = expected_modifiers
        self.return_type = return_type

    def apply(self, file):
        ast = self.file_filter(file)
        if ast is None:
            return []

        feedback = []
        for ast_class in JavaFilter(node_class='class').get_nodes(ast):
            methods_matching = (JavaFilter(node_class='method',
                                           node_return_type=self.return_type,
                                           node_modifiers=['public'])
                                .get_nodes(ast_class))

            for method in methods_matching:
                line, char = method.position
                feedback.append(
                    (line, f'The method {method.name} '
                           f'exposes internal state - keep it encapsulated.'))

        return feedback

    def __str__(self):
        return f'-Access Modifier Check'
