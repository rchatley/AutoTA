from src.entity_relations.DesignPattern import pattern_library
from src.filters.JavaFilter import JavaFilter
from src.rules.AccessModifierCheck import AccessModifierCheck
from src.rules.EncapsulationRule import EncapsulationRule
from src.rules.IdentifierRule import IdentifierRule


def example_template_method_spec():
    task = 'Cryptography Task'
    rules = [EncapsulationRule(scope=('dir', 'main')), IdentifierRule(
        node_filter=JavaFilter(node_class='method',
                               node_annotations=[
                                   'Test'],
                               node_name=r"^test"))]
    patterns = [pattern_library('templateMethod')]

    return Spec(task, rules=rules, structures=patterns)


def camera_exercise_spec():
    task = 'Mock Objects - Camera'
    rules = [
        AccessModifierCheck(scope=('dir', 'src/main/java'),
                            expected_modifiers=['private']),
        AccessModifierCheck(scope=('dir', 'src/main/java'), field_type="Sensor",
                            expected_modifiers=['final']),
        AccessModifierCheck(scope=('dir', 'src/main/java'), field_type="MemoryCard",
                            expected_modifiers=['final']),

        IdentifierRule(scope=('dir', 'src/test/java'),
                       node_filter=JavaFilter(node_class='method', node_annotations=['Test'], node_name=r"^test"))]
    patterns = []

    return Spec(task, rules=rules, structures=patterns)


# def build_spec(spec_file):
#     task = 'Cryptography Task'
#     language = 'java'
#     rules = [EncapsulationRule(scope=('dir', 'main')), IdentifierRule(
#         node_filter=JavaFilter(node_class='method',
#                                node_annotations=[
#                                    'Test'],
#                                node_name=r"^test"))]
#     patterns = [DesignPattern('templateMethod')]
#
#     return Spec(task, language, rules=rules, patterns=patterns)


class Spec:
    def __init__(self, task, rules=None, structures=None):
        self.task = task
        self.rules = rules
        self.structures = structures
