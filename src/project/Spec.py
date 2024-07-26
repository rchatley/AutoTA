from src.entity_relations.CodeStructure import CodeStructure
from src.entity_relations.DesignPattern import pattern_library
from src.entity_relations.ERClasses import Class, Constructor, Field, Interface
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

    structures = [
        CodeStructure("JMock Test",
                      entities={
                          'Test': Class(),
                          'Camera': Class(),
                          'mockery': Field(),
                          'object under test': Field(),
                      },
                      relations={
                          'Test': {
                              'has': ['mockery', 'object under test'],
                          },
                          'object under test': {
                              'isOfType': ['Camera']
                          },
                          # 'mockery': {
                          #     'isOfType': ['JUnitRuleMockery']
                          # }
                      },
                      description="The Camera should be tested by mocking out its collaborators",
                      ),
        CodeStructure("Core Camera implementation",
                      {
                          'Camera': Class(),
                          'Sensor': Interface(info={'name': {'Sensor'}}),
                          'MemoryCard': Interface(info={'name': {'MemoryCard'}}),
                          'constructor': Constructor(info={'modifiers': {'public'}}),
                          'sensor field': Field(info={'modifiers': {'private', 'final'}}),
                          'memory card field': Field(info={'modifiers': {'private', 'final'}}),
                      }, {
                          'Camera': {
                              'has': ['constructor',
                                      'sensor field',
                                      'memory card field'],
                          },
                          'sensor field': {
                              'isOfType': ['Sensor'],
                          },
                          'memory card field': {
                              'isOfType': ['MemoryCard'],
                          },
                      },
                      "The Camera should have fields for the Sensor and MemoryCard", ),
        CodeStructure("WriteListener",
                      {
                          'Camera': Class(),
                          'WriteListener': Interface(),
                      }, {
                          'WriteListener': {
                              'implementedBy': ['Camera'],
                          },
                      },
                      "The Camera should implement the WriteListener interface"),
    ]

    return Spec(task, rules=rules, structures=structures)


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
