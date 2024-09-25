from src.entity_relations.CodeStructure import CodeStructure
from src.entity_relations.DesignPattern import pattern_library
from src.entity_relations.ERClasses import Class, Constructor, Field, Interface
from src.filters.JavaFilter import JavaFilter
from src.rules.AccessModifierCheck import AccessModifierCheck
from src.rules.ClassExtendingSuperclassCheck import ClassExtendingSuperclassCheck
from src.rules.ClassImplementingInterfaceCheck import ClassImplementingInterfaceCheck
from src.rules.EncapsulationRule import EncapsulationRule
from src.rules.IdentifierRule import IdentifierRule
from src.rules.JMockSugarCheck import JMockSugarCheck
from src.rules.MethodWithReturnTypeCheck import MethodWithReturnTypeCheck


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
        AccessModifierCheck(scope=('dir', 'src/main/java'), field_type="List",
                            expected_modifiers=['private', 'final']),
        JMockSugarCheck(scope=('dir', 'src/test/java')),
        MethodWithReturnTypeCheck(scope=('dir', 'src/main/java'), return_type="List"),
        ClassImplementingInterfaceCheck(scope=('dir', 'src/main/java'), interface_type="List"),
        ClassExtendingSuperclassCheck(scope=('dir', 'src/main/java'), superclass_type="ArrayList"),
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

    marking_points = {'CameraTest.java': [
        "There should be basic tests checking that the sensor is turned on and off when the camera is powered on and off",
        "If we are testing turning the camera off, we should power the camera on first",
        "There should be tests checking that the camera can take a picture and store it on the memory card",
        "Each of the tests should check a specific aspect of the camera's functionality",
        "Each behaviour should be tested using mock objects - there shouldn't be any assertions on the state of the camera",
        "There should be minimal duplication of code between tests."
    ],
    'Camera.java': [
        "The Camera class should have a constructor that takes the Sensor and MemoryCard as arguments",
        "The Camera class should have fields to track the power state of the camera",
        "No internal state of the Camera class should be exposed to the outside world - notably the power state",
        "The Camera class should not call the writeComplete() method itself, but should provide an implementation"
        "writeComplete() should trigger a sensor power down if the camera has been powered off while writing",
        "The overall implementation should be neat and concise, with minimal duplication of code",
    ]}

    additional_files = {} #'src/main/java/ic/doc/camera/WriteListener.java'}

    return Spec(task, overview, rules=rules, structures=structures, marking_points=marking_points, additional_files=additional_files)


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
    def __init__(self, task, overview, rules=None, structures=None, marking_points=None, additional_files=set()):
        self.task = task
        self.overview = overview
        self.rules = rules
        self.structures = structures
        self.marking_points = marking_points
        self.additional_files = additional_files
