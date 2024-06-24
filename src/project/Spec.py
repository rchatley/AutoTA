from src.entity_relations.DesignPattern import DesignPattern
from src.filters.JavaFilter import JavaFilter
from src.rules.EncapsulationRule import EncapsulationRule
from src.rules.IdentifierRule import IdentifierRule


def build_spec(spec_file):
    task = 'Cryptography Task'
    language = 'java'
    rules = [EncapsulationRule(scope=('dir', 'main')), IdentifierRule(
        node_filter=JavaFilter(node_class='method',
                               node_annotations=[
                                   'Test'],
                               node_name=r"^test"))]
    patterns = [DesignPattern('templateMethod')]

    return Spec(task, language, rules=rules, patterns=patterns)


class Spec:
    def __init__(self, task, language, rules=None, patterns=None):
        self.task = task
        self.language = language
        self.rules = rules
        self.patterns = patterns
