import javalang

from src.filters.JavaFilter import JavaFilter
from src.project.Feedback import LineFeedback
from src.rules.Rule import Rule


def find_calls(ast_class, method_name, arg_value):
    method_calls = []
    for path, node in ast_class.filter(javalang.tree.MethodInvocation):
        if node.member == method_name:
            for argument in node.arguments:
                # Check if the argument matches the specified value
                if isinstance(argument, javalang.tree.Literal) and argument.value == str(arg_value):
                    # Get the line number from the position attribute
                    method_calls.append(node)
    return method_calls


class JMockSugarCheck(Rule):
    def __init__(self, scope='project'):
        super().__init__(scope)

    def apply(self, file) -> list[LineFeedback]:
        ast = self.file_filter(file)
        if ast is None:
            return []

        feedback: list[LineFeedback] = []
        for ast_class in JavaFilter(node_class='class').get_nodes(ast):

            exactly_zero_calls = find_calls(ast_class, "exactly", 0)

            for call in exactly_zero_calls:
                line, char = call.position
                feedback.append(LineFeedback(line_number=line,
                                             feedback='It would be neater to use never() instead of exactly(0)'))

        return feedback

    def __str__(self):
        return f'-Encapsulation Rule'
