import javalang.tree as java_ast_tree
import networkx as nx
from matplotlib import pyplot as plt

from src.entity_relations.ERClasses import *


def add_node_to_dict(node_dict, key, item):
    if key in node_dict:
        node_dict[key].append(item)
    else:
        node_dict[key] = [item]


def find_in_dict(name_dict, name, origin):
    if name in name_dict:
        if len(name_dict[name]) == 1:
            return name_dict[name][0]
        if len(name_dict[name]) > 1:
            return name_dict[name][1]

    return None


def print_graph(entities, relations):
    G = nx.DiGraph()
    for entity in entities:
        G.add_node(str(entity))

    for relation in relations:
        G.add_edge(str(relation.entity_from), str(relation.entity_to),
                   label=relation.relation_type)

    # Visualize the graph
    pos = nx.spring_layout(G)  # positions for all nodes

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue",
            font_size=10, font_weight="bold", arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 font_color='red')

    plt.title("Entity Relation Graph")
    plt.show()


def build_java_graph(files):
    initial_entities = {}

    relations = []
    entities = []

    file_nodes = {}

    # Initial Pass
    for file in files:
        file_nodes[file] = []
        for node in file.ast.types:
            if isinstance(node, java_ast_tree.ClassDeclaration):
                abstract_class = 'abstract' in node.modifiers
                print(abstract_class)
                class_entity = AbstractClass(node.name, {},
                                             node) if abstract_class else Class(
                    node.name, {}, node)

                entities.append(class_entity)
                file_nodes[file].append(class_entity)
                add_node_to_dict(initial_entities, class_entity.name,
                                 class_entity)

                for member in node.body:
                    if isinstance(member, java_ast_tree.MethodDeclaration):
                        info = {'modifiers': member.modifiers}

                        if abstract_class and 'abstract' in member.modifiers:
                            method_entity = AbstractMethod(member.name, info,
                                                           member)
                        else:
                            method_entity = Method(member.name, info, member)

                        entities.append(method_entity)
                        file_nodes[file].append(method_entity)
                        add_node_to_dict(initial_entities, method_entity.name,
                                         method_entity)
                        relations.append(Has(class_entity, method_entity))

                    elif isinstance(member,
                                    java_ast_tree.FieldDeclaration):
                        info = {'modifiers': member.modifiers,
                                'type': member.type.name}
                        for field in member.declarators:
                            field_entity = Field(field.name, info, member)
                            entities.append(field_entity)
                            file_nodes[file].append(field_entity)
                            add_node_to_dict(initial_entities,
                                             field_entity.name,
                                             field_entity)
                            relations.append(Has(class_entity, field_entity))

                    elif isinstance(member,
                                    java_ast_tree.ConstructorDeclaration):
                        info = {'modifiers': member.modifiers}
                        constructor_entity = Constructor(
                            member.name + ' constructor', info,
                            member)
                        entities.append(constructor_entity)
                        file_nodes[file].append(constructor_entity)
                        add_node_to_dict(initial_entities,
                                         constructor_entity.name,
                                         constructor_entity)
                        relations.append(Has(class_entity, constructor_entity))

            elif isinstance(node, java_ast_tree.InterfaceDeclaration):
                interface_entity = Interface(node.name, {},
                                             node)
                entities.append(interface_entity)
                file_nodes[file].append(interface_entity)
                add_node_to_dict(initial_entities,
                                 interface_entity.name,
                                 interface_entity)
                for member in node.body:
                    if isinstance(member, java_ast_tree.MethodDeclaration):
                        method_entity = AbstractMethod(member.name, {}, member)
                        entities.append(method_entity)
                        file_nodes[file].append(method_entity)
                        add_node_to_dict(initial_entities,
                                         method_entity.name,
                                         method_entity)
                        relations.append(Has(interface_entity, method_entity))

        # print_graph(file_nodes[file], relations)

    for entity in entities:
        node = entity.node
        if entity.type == 'class' or entity.type == 'abstractClass':
            if node.extends is not None:
                related_entity = find_in_dict(initial_entities,
                                              node.extends.name,
                                              entity)
                print(related_entity)
                if related_entity is not None:
                    relations.append(Extends(entity, related_entity))
            if node.implements is not None and len(node.implements) > 0:
                for imp in node.implements:
                    related_entity = find_in_dict(initial_entities,
                                                  imp.name,
                                                  entity)
                    if related_entity is not None:
                        relations.append(Implements(entity, related_entity))
        elif entity.type == 'interface':
            if node.extends is not None and len(node.extends) > 0:
                for ext in node.extends:
                    related_entity = find_in_dict(initial_entities,
                                                  ext.name,
                                                  entity)
                    if related_entity is not None:
                        relations.append(Extends(entity, related_entity))
        elif entity.type == 'field':
            if isinstance(node.type, java_ast_tree.ReferenceType):
                related_entity = find_in_dict(initial_entities,
                                              node.type.name,
                                              entity)
                if related_entity is not None:
                    relations.append(
                        IsOfType(entity, related_entity))
        elif entity.type == 'constructor':
            if node.parameters is not None and len(node.parameters) > 0:
                for param in node.parameters:
                    if isinstance(param.type, java_ast_tree.ReferenceType):
                        related_entity = find_in_dict(initial_entities,
                                                      param.type.name,
                                                      entity)
                        if related_entity is not None:
                            relations.append(
                                ParameterOfType(entity, related_entity))

        elif entity.type == 'method':
            if node.parameters is not None and len(node.parameters) > 0:
                for param in node.parameters:
                    if isinstance(param.type, java_ast_tree.ReferenceType):
                        related_entity = find_in_dict(initial_entities,
                                                      param.type.name,
                                                      entity)
                        if related_entity is not None:
                            relations.append(
                                ParameterOfType(entity, related_entity))
            if node.return_type is not None:
                if isinstance(node.return_type, java_ast_tree.ReferenceType):
                    related_entity = find_in_dict(initial_entities,
                                                  node.return_type.name,
                                                  entity)
                    if related_entity is not None:
                        relations.append(
                            HasReturnType(entity, related_entity))
        elif entity.type == 'abstractMethod':
            if node.parameters is not None and len(node.parameters) > 0:
                for param in node.parameters:
                    if isinstance(param.type, java_ast_tree.ReferenceType):
                        related_entity = find_in_dict(initial_entities,
                                                      param.type.name,
                                                      entity)
                        if related_entity is not None:
                            relations.append(
                                ParameterOfType(entity, related_entity))
    print_graph(entities, relations)
    print(relations)
    return {'entities': entities, 'relations': relations}
