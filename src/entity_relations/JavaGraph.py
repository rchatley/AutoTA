from collections import defaultdict

import javalang.tree as java_ast_tree
import networkx as nx
from matplotlib import pyplot as plt

from src.entity_relations.ERClasses import *
from src.entity_relations.utils import find_in_dict
from src.project.JavaFile import JavaFile


def print_graph(entities, relations):
    entity_colors = {
        'class': 'skyblue',
        'abstractClass': 'lightgreen',
        'interface': 'lightcoral',
        'constructor': 'lightyellow',
        'method': 'lightpink',
        'abstractMethod': 'lightgray',
        'field': 'lightblue'
    }
    graph = nx.DiGraph()

    # Add nodes to the graph
    for entity in entities:
        graph.add_node(str(entity), entity_type=entity.type)

    # Add edges to the graph
    for relation in relations:
        graph.add_edge(str(relation.entity_from), str(relation.entity_to),
                       label=relation.relation_type)

    # Use the spring layout to position nodes
    pos = nx.spring_layout(graph, k=1, iterations=100)

    plt.figure(figsize=(12, 8))

    for node in graph.nodes:
        if 'entity_type' not in graph.nodes[node]:
            print(node)

    # Draw the nodes and edges
    node_colors = [entity_colors[graph.nodes[node]['entity_type']] for node in
                   graph.nodes]
    nx.draw(graph, pos, with_labels=True, node_size=3000,
            node_color=node_colors,
            font_size=10, font_weight="bold", arrows=True)

    # Draw the edge labels
    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels,
                                 font_color='red', font_size=8, label_pos=0.5,
                                 rotate=False)

    # Adjust positions to avoid overlap with edge labels
    for (node, (x, y)) in pos.items():
        dx = 0.02  # Offset for x
        dy = 0.02  # Offset for y
        pos[node] = (x + dx, y + dy)

    plt.title("Entity Relation Graph")
    plt.show()


def first_pass(java_file: JavaFile, first_pass_dict):

    package_name = java_file.package_name()

    full_file_name = java_file.full_file_path()

    file_entities = []
    file_relations = []

    for class_node in java_file.ast.types:
        if isinstance(class_node, java_ast_tree.ClassDeclaration):
            abstract_class = 'abstract' in class_node.modifiers
            info = {'name': class_node.name}
            class_entity = AbstractClass(info=info, node=class_node,
                                         package=package_name,
                                         file=full_file_name) if abstract_class else Class(
                info=info, node=class_node, package=package_name,
                file=full_file_name)

            file_entities.append(class_entity)
            first_pass_dict[class_node.name].append(class_entity)

            for member_node in class_node.body:
                if isinstance(member_node, java_ast_tree.MethodDeclaration):
                    info = {'modifiers': member_node.modifiers,
                            'name': member_node.name}
                    if abstract_class and 'abstract' in member_node.modifiers:
                        method_entity = AbstractMethod(info=info,
                                                       node=member_node,
                                                       package=package_name,
                                                       file=full_file_name)
                    else:
                        method_entity = Method(info=info, node=member_node,
                                               package=package_name,
                                               file=full_file_name)

                    file_entities.append(method_entity)
                    first_pass_dict[member_node.name].append(method_entity)
                    file_relations.append(Has(class_entity, method_entity))
                elif isinstance(member_node, java_ast_tree.FieldDeclaration):
                    for field in member_node.declarators:
                        info = {'modifiers': member_node.modifiers,
                                'name': field.name,
                                'type': member_node.type.name }
                        field_entity = Field(info=info, node=member_node,
                                             package=package_name,
                                             file=full_file_name)
                        file_entities.append(field_entity)
                        first_pass_dict[field.name].append(field_entity)
                        file_relations.append(Has(class_entity, field_entity))
                elif isinstance(member_node,
                                java_ast_tree.ConstructorDeclaration):
                    info = {'modifiers': member_node.modifiers,
                            'name': f'{class_node.name} Constructor'}
                    constructor_entity = Constructor(info=info,
                                                     node=member_node,
                                                     package=package_name,
                                                     file=full_file_name)
                    file_entities.append(constructor_entity)
                    first_pass_dict[info['name']].append(constructor_entity)
                    file_relations.append(
                        Has(class_entity, constructor_entity))

        elif isinstance(class_node, java_ast_tree.InterfaceDeclaration):
            info = {'name': class_node.name}
            interface_entity = Interface(info=info, node=class_node,
                                         package=package_name,
                                         file=full_file_name)

            file_entities.append(interface_entity)
            first_pass_dict[class_node.name].append(interface_entity)

            for member_node in class_node.body:
                info = {'name': member_node.name,
                        'modifiers': member_node.modifiers}
                if isinstance(member_node, java_ast_tree.MethodDeclaration):
                    method_entity = AbstractMethod(info=info, node=member_node,
                                                   package=package_name,
                                                   file=full_file_name)

                    file_entities.append(method_entity)
                    first_pass_dict[member_node.name].append(method_entity)
                    file_relations.append(Has(interface_entity, method_entity))

        return file_entities, file_relations


def build_code_graph(files, display=False):
    entities = []
    relations = []

    first_pass_dict = defaultdict(list)

    # Initial Pass
    for file in files:
        file_entities, file_relations = first_pass(file, first_pass_dict)
        entities.extend(file_entities)
        relations.extend(file_relations)

        if display:
            print_graph(file_entities, file_relations)

    for entity in entities:
        node = entity.node
        if entity.type == 'class' or entity.type == 'abstractClass':
            # AbstractClass/Class - Extends
            if node.extends is not None:
                related_entity = find_in_dict(node.extends.name,
                                              first_pass_dict, entity)
                if related_entity is not None:
                    relations.append(Extends(entity, related_entity))
            # AbstractClass/Class - Implements
            if node.implements is not None and len(node.implements) > 0:
                for imp in node.implements:
                    related_entity = find_in_dict(imp.name, first_pass_dict,
                                                  entity)
                    if related_entity is not None:
                        relations.append(Implements(entity, related_entity))
        elif entity.type == 'interface':
            # Interface - Extends
            if node.extends is not None and len(node.extends) > 0:
                for ext in node.extends:
                    related_entity = find_in_dict(ext.name, first_pass_dict,
                                                  entity)
                    if related_entity is not None:
                        relations.append(Extends(entity, related_entity))
        elif entity.type == 'abstractMethod' or entity.type == 'method':
            # AbstractMethod/Method - Parameter
            if node.parameters is not None and len(node.parameters) > 0:
                for param in node.parameters:
                    if isinstance(param.type, java_ast_tree.ReferenceType):
                        related_entity = find_in_dict(param.type.name,
                                                      first_pass_dict, entity)
                        if related_entity is not None:
                            relations.append(
                                ParameterOfType(entity, related_entity))
            # AbstractMethod/Method - ReturnType
            if node.return_type is not None:
                if isinstance(node.return_type,
                              java_ast_tree.ReferenceType):
                    related_entity = find_in_dict(node.return_type.name,
                                                  first_pass_dict, entity)
                    if related_entity is not None:
                        relations.append(
                            HasReturnType(entity, related_entity))
            if entity.type == 'method':
                # Method - Overrides
                for owner in entity.relations['composes']:
                    for interface_entity in owner.relations['implements']:
                        for member in interface_entity.relations['has']:
                            if member.type == 'abstractMethod':
                                # ADD TYPE CHECK
                                if member.info['name'] == entity.info['name']:
                                    relations.append(Overrides(entity, member))
                    for interface_entity in owner.relations['extends']:
                        for member in interface_entity.relations['has']:
                            if member.type in ['abstractMethod', 'method']:
                                # ADD TYPE CHECK
                                if member.info['name'] == entity.info['name']:
                                    relations.append(Overrides(entity, member))
                # Method - Invokes
                for member in node.body:
                    for _, member_node in member:
                        if isinstance(member_node,
                                      java_ast_tree.MethodInvocation):
                            related_entity = find_in_dict(member_node.member,
                                                          first_pass_dict,
                                                          entity)
                            if related_entity is not None:
                                relations.append(
                                    Invokes(entity, related_entity))
        elif entity.type == 'field':
            # Field - Type
            if isinstance(node.type, java_ast_tree.ReferenceType):
                related_entity = find_in_dict(node.type.name, first_pass_dict,
                                              entity)
                if related_entity is not None:
                    relations.append(
                        IsOfType(entity, related_entity))
        elif entity.type == 'constructor':
            # Constructor - Parameters
            if node.parameters is not None and len(node.parameters) > 0:
                for param in node.parameters:
                    if isinstance(param.type, java_ast_tree.ReferenceType):
                        related_entity = find_in_dict(param.type.name,
                                                      first_pass_dict, entity)
                        if related_entity is not None:
                            relations.append(
                                ParameterOfType(entity, related_entity))
            # Constructor - Invokes
            for member in node.body:
                for _, member_node in member:
                    if isinstance(member_node,
                                  java_ast_tree.MethodInvocation):
                        related_entity = find_in_dict(member_node.member,
                                                      first_pass_dict,
                                                      entity)
                        if related_entity is not None:
                            relations.append(
                                Invokes(entity, related_entity))

    if display:
        print_graph(entities, relations)

    return {'entities': entities, 'relations': relations}
