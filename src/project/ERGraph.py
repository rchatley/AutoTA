import javalang.tree as java_ast_tree


class ERGraph:
    def __init__(self, lang, files):
        self.lang = lang
        self.files = files

        if lang == 'java':
            self.graph = self.build_java_graph()
        elif lang == 'python':
            self.graph = self.build_python_graph()
        else:
            self.graph = None

    def build_java_graph(self):
        graph = {'nodes': {}, 'relations': {}}
        for file in self.files:
            for _, node in file.ast:
                if isinstance(node, java_ast_tree.ClassDeclaration):
                    class_name = node.name
                    if 'abstract' in node.modifiers:
                        print('AbstractClass: ' + class_name)
                    else:
                        print('Class: ' + class_name)

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

                elif isinstance(node, java_ast_tree.InterfaceDeclaration):
                    if node.extends is not None and len(
                            node.extends) > 0:
                        for implements in node.extends:
                            interface = implements.name
                            print(' -Extends: ' + interface)
                    for member in node.body:
                        if isinstance(member, java_ast_tree.MethodDeclaration):
                            print(' -Method: ' + member.name)
                            if member.return_type is not None:
                                print(
                                    ' ---Return Type: ' + member.return_type.name)

        return graph

    def build_python_graph(self):
        return {self.files}
