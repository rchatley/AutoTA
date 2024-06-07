import ast as python_ast

from review.filters.JavaFilter import JavaFilter
from review.rules.Rule import Rule


# Checks that all classes within scope are Encapsulated
class EncapsulationRule(Rule):
    def __init__(self, scope='project', getters=False, setters=False):
        super().__init__(scope)
        self._getters = getters
        self._setters = setters

    def apply(self, file):
        ast = self.file_filter(file)
        if file is None:
            return []

        feedback = []
        if file.language == 'java':
            for ast_class in JavaFilter(node_class='class').get_nodes(ast):
                visible_fields = JavaFilter(node_class='field',
                                            node_modifiers=['private'],
                                            negatives=[
                                                'node_modifiers']).get_nodes(
                    ast_class)

                for field in visible_fields:
                    line, char = field.position
                    feedback.append(
                        f'{file.file_name}:{line}:{char}: In class'
                        f' {ast_class.name}, the {field.declarators[0].name} '
                        f'field is not private')

                if self._getters:
                    pass

                if self._setters:
                    pass
        elif file.language == 'python':
            class PublicFieldVisitor(python_ast.NodeVisitor):
                def __init__(self):
                    self.current_class = None
                    self.public_fields = []

                def visit_ClassDef(self, node):
                    self.current_class = node.name
                    self.generic_visit(node)
                    self.current_class = None

                def visit_Assign(self, node):
                    if self.current_class:
                        for target in node.targets:
                            if not target.attr.startswith('_'):
                                self.public_fields.append((target.attr,
                                                           target.lineno,
                                                           target.col_offset,
                                                           self.current_class))
                    self.generic_visit(node)

            visitor = PublicFieldVisitor()
            visitor.visit(ast)

            for field_name, line, char, class_name in visitor.public_fields:
                feedback.append(
                    f'{file.file_name}:{line}:{char}: In class'
                    f' {class_name}, the {field_name} '
                    f'field is not private')

        return feedback
