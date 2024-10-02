from src.filters.Filter import get_node_name
from src.project.Feedback import LineFeedback
from src.rules.Rule import Rule


# Checks that all nodes within scope follow naming convention
class IdentifierRule(Rule):
    def __init__(self, scope='project', node_filter=None, feedback_msg=None):
        super().__init__(scope)
        self.feedback_msg = feedback_msg
        self.node_filter = node_filter

    def apply(self, file) -> list[LineFeedback]:
        ast = self.file_filter(file)
        if ast is None or self.node_filter is None:
            return []

        feedback = []
        for node in self.node_filter.get_nodes(ast):
            line, char = node.position
            name = get_node_name(node)

            if self.feedback_msg is not None:
                feedback.append(
                    (line, self.feedback_msg))
            else:
                feedback.append(
                    LineFeedback(line_number=line,
                                 feedback=f'The {self.node_filter.node_class}, {name}, does not follow the specified naming convention.'))

        return feedback

    def __str__(self):
        return f'-Identifer Rule'
