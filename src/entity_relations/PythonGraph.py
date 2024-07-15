import ast
import os

from src.entity_relations.ERClasses import *
from src.entity_relations.utils import add_node_to_dict, find_in_dict


def process_node(node, file_entities, file_relations, first_pass_dict,
                 parent=None, package_name=None, full_file_name=None):
    if isinstance(node, ast.ClassDef):
        info = {'name': node.name}
        class_entity = Class(info=info, node=node, package=package_name,
                             file=full_file_name)
        file_entities.append(class_entity)
        add_node_to_dict(first_pass_dict, node.name, class_entity)
        if parent:
            file_relations.append(Has(parent, class_entity))

        for member in node.body:
            process_node(member, file_entities, file_relations,
                         first_pass_dict, parent=class_entity,
                         package_name=package_name,
                         full_file_name=full_file_name)

    elif isinstance(node, ast.FunctionDef):
        info = {'name': node.name}
        method_entity = Method(info=info, node=node, package=package_name,
                               file=full_file_name)
        file_entities.append(method_entity)
        add_node_to_dict(first_pass_dict, node.name, method_entity)
        if parent:
            file_relations.append(Has(parent, method_entity))

        for stmt in node.body:
            if isinstance(stmt, ast.Call):
                if isinstance(stmt.func, ast.Attribute):
                    called_entity = find_in_dict(stmt.func.attr,
                                                 first_pass_dict,
                                                 method_entity)
                    if called_entity:
                        file_relations.append(
                            Invokes(method_entity, called_entity))
                elif isinstance(stmt.func, ast.Name):
                    called_entity = find_in_dict(stmt.func.id, first_pass_dict,
                                                 method_entity)
                    if called_entity:
                        file_relations.append(
                            Invokes(method_entity, called_entity))


def first_pass(file, first_pass_dict):
    package_name = None
    full_file_name = os.path.join(file.relative_path, file.file_name)

    file_entities = []
    file_relations = []

    for node in file.ast.body:
        process_node(node, file_entities, file_relations, first_pass_dict,
                     package_name=package_name, full_file_name=full_file_name)

    return file_entities, file_relations


def build_python_graph(files):
    entities = []
    relations = []
    first_pass_dict = {}

    # Initial Pass
    for file in files:
        file_entities, file_relations = first_pass(file, first_pass_dict)
        entities.extend(file_entities)
        relations.extend(file_relations)
    # Second Pass
    for entity in entities:
        node = entity.node
        if entity.type == 'class' or entity.type == 'abstractClass':
            for base in node.bases:
                if isinstance(base, ast.Name):
                    related_entity = find_in_dict(base.id, first_pass_dict,
                                                  entity)
                    if related_entity:
                        relations.append(Extends(entity, related_entity))
        elif entity.type == 'method':
            if node.args.args:
                for param in node.args.args:
                    if isinstance(param.annotation, ast.Name):
                        related_entity = find_in_dict(param.annotation.id,
                                                      first_pass_dict, entity)
                        if related_entity:
                            relations.append(
                                ParameterOfType(entity, related_entity))

            if isinstance(node.returns, ast.Name):
                related_entity = find_in_dict(node.returns.id, first_pass_dict,
                                              entity)
                if related_entity:
                    relations.append(HasReturnType(entity, related_entity))

    return {'entities': entities, 'relations': relations}
