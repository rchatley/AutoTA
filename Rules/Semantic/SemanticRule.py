from Rules.SpecRule import SpecRule
from javalang import tree

node_dict = {'node': tree.Declaration, 'method': tree.MethodDeclaration, 'class': tree.ClassDeclaration,
             'field': tree.FieldDeclaration, 'constructor': tree.ConstructorDeclaration}


class SemanticRule(SpecRule):
    def __init__(self, scope='project', node_info=None, rule_modifiers=None):
        super().__init__(scope=scope)
        if node_info is None:
            node_info = {'annotation': None, 'modifiers': None, 'node': 'node'}

        if rule_modifiers is None:
            rule_modifiers = {'frequency': 'every', 'positivity': True}

        self.annotation = node_info['annotation']
        self.modifiers = node_info['modifiers']
        self.node = node_info['node']
        self.node_tree_class = node_dict[self.node]

        self.frequency = rule_modifiers['frequency']
        self.positivity = rule_modifiers['positivity']

    def build_rule(self):
        def rule(review_file):
            if not self.filter(review_file):
                return []

            ast = review_file.ast

            filtered_ast = ast.filter(self.node_tree_class)

            return self.traversal(filtered_ast, self.positivity, self.frequency)

        return rule
