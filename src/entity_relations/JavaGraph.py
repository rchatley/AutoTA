import javalang.tree as java_ast_tree


def build_java_graph(files):
    graph = {'nodes': {}, 'relations': {}}
    for file in files:
        for _, node in file.ast:
            if isinstance(node, java_ast_tree.ClassDeclaration):
                build_class_graph(node)
            elif isinstance(node, java_ast_tree.InterfaceDeclaration):
                build_interface_graph(node)

    return graph


def build_class_graph(node):
    if node.extends is not None:
        superclass = node.extends.name
        print(' -Extends: ' + superclass)

    if node.implements is not None and len(
            node.implements) > 0:
        for implements in node.implements:
            interface = implements.name
            print(' -Implements: ' + interface)

    for member in node.body:
        if isinstance(member, java_ast_tree.MethodDeclaration):
            print(' -Method: ' + member.name)
            if member.return_type is not None:
                print(
                    ' ---Return Type: ' + member.return_type.name)
        elif isinstance(member,
                        java_ast_tree.FieldDeclaration):
            for field in member.declarators:
                print(' -Field: ' + field.name)
        elif isinstance(member,
                        java_ast_tree.ConstructorDeclaration):
            print(' -Constructor: ' + member.name)

        if 'abstract' in node.modifiers:
            build_abstract_class_graph(member)


def build_abstract_class_graph(node):
    pass

def build_interface_graph(node):
    if node.extends is not None and len(
            node.extends) > 0:
        for implements in node.extends:
            interface = implements.name
            print(' -Extends: ' + interface)
    for member in node.body:
        if isinstance(member, java_ast_tree.MethodDeclaration):
            build_method_graph(member)


def build_method_graph(member):
    print(' -Method: ' + member.name)
    if member.return_type is not None:
        print(
            ' ---Return Type: ' + member.return_type.name)
