from src.filters.JavaFilter import JavaFilter
from src.patterns.DesignPattern import DesignPattern
from src.rules.EncapsulationRule import EncapsulationRule
from src.rules.IdentifierRule import IdentifierRule


def sample_spec():
    return Spec('java',
                [EncapsulationRule(),
                 IdentifierRule(node_filter=JavaFilter(node_class='method',
                                                       node_annotations=[
                                                           'Test'],
                                                       node_name=r"^test"))],
                [DesignPattern('singleton')])


def get_task_spec(task_number, task_language):
    java_spec_dict = {1: Spec('java',
                              [EncapsulationRule(),
                               IdentifierRule(
                                   node_filter=JavaFilter(node_class='method',
                                                          node_annotations=[
                                                              'Test'],
                                                          node_name=r"^test"))]),
                      3: None,
                      4: None,
                      7: None}
    python_spec_dict = {1: None,
                        3: None,
                        4: None,
                        7: None}
    lang_spec_dict = {'java': java_spec_dict, 'python': python_spec_dict}

    return lang_spec_dict[task_language][task_number]


def build_spec(spec_file):
    return Spec('java')


class Spec:
    def __init__(self, language, rules=None, patterns=None):
        self.language = language
        self.rules = rules
        self.patterns = patterns
