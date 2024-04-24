from Rules.SpecRule import SpecRule


class SyntacticRule(SpecRule):
    def __init__(self, scope='project'):
        super().__init__(scope=scope)

    def build_rule(self):
        def rule(review_file):
            if not self.filter(review_file):
                return []

            return self.traversal(review_file)

        return rule
