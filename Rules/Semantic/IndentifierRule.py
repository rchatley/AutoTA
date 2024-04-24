import re

from Rules.Semantic.SemanticRule import SemanticRule


class IdentifierRule(SemanticRule):
    def __init__(self, pattern='.*', scope='project', node_info=None, rule_modifiers=None):
        super().__init__(scope, node_info, rule_modifiers)
        self.pattern = pattern
        self.traversal = self.build_traversal()

        self.rule = self.build_rule()

    def __str__(self):
        modifier_string = 'must' if self.positivity else 'must not'
        prefix = self.frequency.capitalize() if self.scope == 'project' else f'In {self.scope[0]} {self.scope[1]}, {self.frequency}'

        return f'{prefix} {self.node} {modifier_string} have an identifier of the format {self.pattern}'

    def build_traversal(self):
        def traversal(ast, positivity, frequency):
            issues = []
            for path, node in ast:
                if positivity:
                    if not re.match(self.pattern, node.name):
                        issues.append(f"({node.position[0]}, {node.position[1]}) | {self}")
                else:
                    if re.match(self.pattern, node.name):
                        issues.append(f"({node.position[0]}, {node.position[1]}) | {self}")

            return issues

        return traversal
