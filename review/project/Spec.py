from review.patterns.DesignPattern import DesignPattern
from review.rules.EncapsulationRule import EncapsulationRule
from review.rules.IdentifierRule import IdentifierRule


def sample_spec():
    return Spec('java',
                [EncapsulationRule(), IdentifierRule(node_class='method',
                                                     annotations=['Test'],
                                                     name_format=r"^test")],
                [DesignPattern('singleton')])


def get_task_spec(task_number, task_language):
    java_spec_dict = {1: Spec('java',
                              [EncapsulationRule(),
                               IdentifierRule(node_class='method',
                                              annotations=['Test'],
                                              name_format=r"^test")]),
                      3: None,
                      4: None,
                      7: None}
    python_spec_dict = {1: None,
                        3: None,
                        4: None,
                        7: None}
    lang_spec_dict = {'java': java_spec_dict, 'python': python_spec_dict}

    return lang_spec_dict[task_language][task_number]


class Spec:
    def __init__(self, language, rules=None, patterns=None):
        self.language = language
        self.rules = rules
        self.patterns = patterns
