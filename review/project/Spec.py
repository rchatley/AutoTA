from review.rules.EncapsulationRule import EncapsulationRule
from review.rules.IndentifierRule import IdentifierRule


def sample_spec():
    return Spec('java',
                [EncapsulationRule(), IdentifierRule(node_class='method',
                                                     annotations=['Test'],
                                                     name_format=r"^test")],
                ['singleton'])


class Spec:
    def __init__(self, language, rules, patterns):
        self.language = language
        self.rules = rules
        self.patterns = patterns
