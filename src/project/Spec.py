from src.entity_relations.CodeStructure import CodeStructure
from src.entity_relations.DesignPattern import pattern_library
from src.entity_relations.ERClasses import Class, Constructor, Field, Interface
from src.filters.JavaFilter import JavaFilter
from src.rules.AccessModifierCheck import AccessModifierCheck
from src.rules.EncapsulationRule import EncapsulationRule
from src.rules.IdentifierRule import IdentifierRule
from src.rules.JMockSugarCheck import JMockSugarCheck


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
    overview = ("This idea with this task was to test the behaviour of the camera class "
                "by mocking out its collaborators.")
    rules = [
        AccessModifierCheck(scope=('dir', 'src/main/java'),
                            expected_modifiers=['private']),
        AccessModifierCheck(scope=('dir', 'src/main/java'), field_type="Sensor",
                            expected_modifiers=['private', 'final']),
        AccessModifierCheck(scope=('dir', 'src/main/java'), field_type="MemoryCard",
                            expected_modifiers=['private', 'final']),
        JMockSugarCheck(scope=('dir', 'src/test/java')),
        IdentifierRule(scope=('dir', 'src/test/java'),
                       node_filter=JavaFilter(node_class='method', node_annotations=['Test'], node_name=r"^test"))]

    structures = [
        CodeStructure("JMock Test",
                      entities={
                          'Test': Class(),
                          'Camera': Class(),
                          'mockery': Field(
                              info={'modifiers': {'public'}, 'type': 'JUnitRuleMockery', 'annotations': {'Rule'}}),
                          'object under test': Field(),
                      },
                      relations={
                          'Test': {
                              'has': ['mockery', 'object under test'],
                          },
                          'object under test': {
                              'isOfType': ['Camera']
                          },
                      },
                      description="Camera should be tested by mocking out its collaborators",
                      ),
        CodeStructure("Core Camera implementation",
                      {
                          'Camera': Class(),
                          'constructor': Constructor(info={'modifiers': {'public'}}),
                          'sensor field': Field(info={'modifiers': {'private', 'final'}, 'type': 'Sensor'}),
                          'memory card field': Field(info={'modifiers': {'private', 'final'}, 'type': 'MemoryCard'}),
                      }, {
                          'Camera': {
                              'has': ['constructor',
                                      'sensor field',
                                      'memory card field'],
                          }
                      },
                      "Camera should encapsulate fields for the Sensor and MemoryCard", ),
        CodeStructure("WriteListener",
                      {
                          'Camera': Class(),
                          'WriteListener': Interface(),
                      }, {
                          'WriteListener': {
                              'implementedBy': ['Camera'],
                          },
                      },
                      "Camera should implement the WriteListener interface as a callback mechanism"),
    ]

    additional_files = {'src/main/java/ic/doc/camera/WriteListener.java'}

    return Spec(task, overview, rules=rules, structures=structures, additional_files=additional_files)


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
    def __init__(self, task, overview, rules=None, structures=None, additional_files=set()):
        self.task = task
        self.overview = overview
        self.rules = rules
        self.structures = structures
        self.additional_files = additional_files
