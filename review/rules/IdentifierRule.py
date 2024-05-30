from review.filters.JavaFilter import JavaFilter
from review.rules.Rule import Rule


# Checks that all nodes within scope follow naming convention
class IdentifierRule(Rule):
    def __init__(self, scope='project', node_class='node', name_format='.*',
                 annotations=None):
        super().__init__(scope)
        self.node_name = name_format
        self.node_class = node_class
        self.annotations = annotations

    def apply(self, file):
        ast = self.filter(file)
        if file is None:
            return []

        feedback = []
        for node in JavaFilter(node_class=self.node_class,
                               node_name=self.node_name,
                               node_annotations=self.annotations).get_nodes(
            ast):

            line, char = node.position
            if hasattr(node, 'name'):
                name = node.name
            else:
                name = node.declarators[0].name
            feedback.append(
                f'{file.file_name}:{line}:{char}: The {self.node_class}, '
                f'{name}, does not follow the specified naming convention.')

        return feedback
