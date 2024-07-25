from src.entity_relations.CodeStructure import CodeStructure
from src.entity_relations.ERClasses import *


def pattern_library(pattern_name: str) -> CodeStructure:
    pattern_dict = {
        'singleton':
            CodeStructure("Singleton",
                          {
                              'singleton': Class(),
                              'private constructor': Constructor(
                                  info={'modifiers': {'private'}}),
                              'private instance': Field(
                                  info={'modifiers': {'private'}}),
                              'get_instance': Method()
                          }, {
                              'singleton': {
                                  'has': ['private constructor',
                                          'private instance',
                                          'get_instance']
                              },
                              'private instance': {
                                  'isOfType': ['singleton']
                              },
                              'get_instance': {
                                  'hasReturnType': ['singleton']
                              }
                          },
                          'The Singleton pattern ensures that a class has only one instance'
                          ' and provides a global point of access to it.'
                          ),
        'templateMethod':
            CodeStructure("Template Method",
                          {
                              'template': AbstractClass(),
                              'abstract method': AbstractMethod(),
                              'template method': Method(),
                              'subclass': Class(),
                              'override': Method()
                          },
                          {
                              'template': {
                                  'has': ['abstract method', 'template method']
                              },
                              'subclass': {
                                  'extends': ['template'],
                                  'has': ['override']
                              },
                              'template method': {
                                  'invokes': ['abstract method']
                              }
                          },
                          'The Template Method pattern defines the skeleton of an algorithm in an abstract '
                          'superclass, together with hook methods overridden to specialise behaviour in subclasses.'),
        'strategy':
            CodeStructure("Strategy",
                          {
                              'context': Class(),
                              'context_field': Field(),
                              'strategy': Interface(),
                              'strategy_method': AbstractMethod(),
                              'concrete_strategy': Class(),
                              'concrete_method': Method()
                          },
                          {
                              'context': {
                                  'has': ['context_field']
                              },
                              'strategy': {
                                  'has': ['strategy_method']
                              },
                              'concrete_strategy': {
                                  'implements': ['strategy']
                              },
                              'context_field': {
                                  'isOfType': ['strategy']
                              },
                              'concrete_method': {
                                  'overrides': ['strategy_method']
                              }
                          },
                          'The Strategy pattern defines a family of algorithms, combining '
                          'them using composition and allowing clients to choose the most suitable one.')}

    return pattern_dict[pattern_name]
