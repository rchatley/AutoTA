from javalang import tree

from Rules.Semantic.SemanticRule import SemanticRule


class EncapsulationRule(SemanticRule):
    def __init__(self, scope='project', node_info=None, rule_modifiers=None):
        if node_info is None:
            node_info = {'annotation': None, 'modifiers': None, 'node': 'class'}

        super().__init__(scope, node_info, rule_modifiers)
        self.traversal = self.build_traversal()

        self.rule = self.build_rule()

    def __str__(self):
        modifier_string = 'must' if self.positivity else 'must not'
        prefix = self.frequency.capitalize() if self.scope == 'project' else f'In {self.scope[0]} {self.scope[1]}, {self.frequency}'

        return f'{prefix} {self.node} {modifier_string} be encapsulated'

    def build_traversal(self):
        def traversal(ast, positivity, frequency):
            issues = []
            for path, node in ast:
                for member in node.body:
                    if isinstance(member, tree.FieldDeclaration):
                        if positivity:
                            if 'private' not in member.modifiers:
                                issues.append(f"({node.position[0]}, {node.position[1]}) | {self}")
                        else:
                            if 'private' in member.modifiers:
                                issues.append(f"({node.position[0]}, {node.position[1]}) | {self}")
            return issues

        return traversal
