from src.entity_relations.DesignPattern import DesignPattern
from src.filters.JavaFilter import JavaFilter
from src.rules.EncapsulationRule import EncapsulationRule
from src.rules.IdentifierRule import IdentifierRule


def build_spec(spec_file):
    language = 'java'
    rules = [EncapsulationRule(scope=('dir', 'src/main')), IdentifierRule(
        node_filter=JavaFilter(node_class='method',
                               node_annotations=[
                                   'Test'],
                               node_name=r"^test"))]
    patterns = [DesignPattern('templateMethod')]

    return Spec('java', rules=rules, patterns=patterns)


class Spec:
    def __init__(self, language, rules=None, patterns=None):
        self.language = language
        self.rules = rules
        self.patterns = patterns
