import ast

from src.entity_relations.ERClasses import *


def add_node_to_dict(node_dict, key, item):
    if key in node_dict:
        node_dict[key].append(item)
    else:
        node_dict[key] = [item]


def build_python_graph(files):
    initial_entities = {}
    relations = []
    entities = []

    for file in files:
        for node in ast.walk(file.ast):
            if isinstance(node, ast.ClassDef):
                class_entity = Class(node.name, node)
                entities.append(class_entity)
                add_node_to_dict(initial_entities, class_entity.name,
                                 class_entity)
                for member in node.body:
                    if isinstance(member, ast.FunctionDef):
                        method_entity = Method(member.name, member)
                        entities.append(method_entity)
                        add_node_to_dict(initial_entities,
                                         method_entity.name, method_entity)
                        relations.append(Has(class_entity, method_entity))
                    elif isinstance(member, ast.Assign):
                        for target in member.targets:
                            if isinstance(target, ast.Name):
                                var_entity = Field(target.id, target)
                                entities.append(var_entity)
                                add_node_to_dict(initial_entities,
                                                 var_entity.name,
                                                 var_entity)
                                relations.append(
                                    Has(class_entity, var_entity))
