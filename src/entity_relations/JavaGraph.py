import javalang.tree as java_ast_tree

from src.entity_relations.ERClasses import *


def build_java_graph(files):
    relations = []
    entities = []

    # Initial Pass
    for file in files:
        for node in file.ast.types:
            if isinstance(node, java_ast_tree.ClassDeclaration):
                abstract_class = 'abstract' in node.modifiers
                print(node)
                class_entity = AbstractClass(node.name, {},
                                             node) if abstract_class else Class(
                    node.name, {}, node)

                entities.append(class_entity)

                for member in node.body:
                    if isinstance(member, java_ast_tree.MethodDeclaration):
                        if abstract_class:
                            if 'abstract' in member.modifiers:
                                method_entity = AbstractMethod(member.name, {},
                                                               member)
                            else:
                                method_entity = Method(member.name, {}, member)
                        else:
                            method_entity = Method(member.name, {}, member)

                        entities.append(method_entity)
                        relations.append(Has(class_entity, method_entity))

                    elif isinstance(member,
                                    java_ast_tree.FieldDeclaration):
                        info = {'modifiers': [member.modifiers],
                                'type': member.type.name}
                        for field in member.declarators:
                            field_entity = Field(field.name, info, member)
                            entities.append(field_entity)
                            relations.append(Has(class_entity, field_entity))

                    elif isinstance(member,
                                    java_ast_tree.ConstructorDeclaration):
                        constructor_entity = Constructor(member.name, {},
                                                         member)
                        entities.append(constructor_entity)
                        relations.append(Has(class_entity, constructor_entity))

            elif isinstance(node, java_ast_tree.InterfaceDeclaration):
                interface_entity = Interface(node.name, {},
                                             node)
                entities.append(interface_entity)
                for member in node.body:
                    if isinstance(member, java_ast_tree.MethodDeclaration):
                        method_entity = AbstractMethod(member.name, {}, member)
                        entities.append(method_entity)
                        relations.append(Has(interface_entity, method_entity))

    return {'entities': entities, 'relations': relations}
