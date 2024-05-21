import re
from javalang import tree


class JavaFilter:
    def __init__(self, node_class=None, node_name=None, node_modifiers=None,
                 node_annotations=None, node_extends=None,
                 node_implements=None,
                 node_type=None, node_return_type=None):
        self.node_class = node_class
        self.node_name = node_name
        self.node_modifiers = node_modifiers
        self.node_annotations = node_annotations
        self.node_extends = node_extends
        self.node_implements = node_implements
        self.node_type = node_type
        self.node_return_type = node_return_type

        self.class_map = {'node': tree.Node,
                          'class': tree.ClassDeclaration,
                          'method': tree.MethodDeclaration,
                          'method_invocation': tree.MethodInvocation,
                          'field': tree.FieldDeclaration,
                          'constructor': tree.ConstructorDeclaration,
                          'interface': tree.InterfaceDeclaration,
                          'enum': tree.EnumDeclaration}

    def filter_node_class(self, node):

        return isinstance(node, self.class_map[self.node_class])

    def filter_node_name(self, node):
        if self.node_name is None:
            return True
        if not hasattr(node, 'name'):
            if hasattr(node, 'declarators'):
                comp_name = node.declarators[0].name
            else:
                return False
        else:
            comp_name = node.name
        return re.match(self.node_name, comp_name)

    def filter_node_modifiers(self, node):
        if self.node_modifiers is None or len(self.node_modifiers) == 0:
            return True
        if not hasattr(node, 'modifiers') or node.modifiers is None:
            return False
        return set(self.node_modifiers).issubset(set(node.modifiers))

    def filter_node_annotations(self, node):
        if self.node_annotations is None or len(self.node_annotations) == 0:
            return True
        if not hasattr(node, 'annotations'):
            return False
        annotation_names = [annotation.name for annotation in node.annotations]
        return set(self.node_annotations).issubset(set(annotation_names))

    def filter_node_extends(self, node):
        if self.node_extends is None:
            return True
        if not hasattr(node, 'extends'):
            return False
        return node.extends and node.extends.name == self.node_extends

    def filter_node_implements(self, node):
        if self.node_implements is None or len(self.node_implements) == 0:
            return True
        if not hasattr(node, 'implements') or not node.implements:
            return False
        implements_names = [implements.name for implements in node.implements]
        return set(self.node_implements).issubset(set(implements_names))

    def filter_node_type(self, node):
        if self.node_type is None:
            return True
        if not hasattr(node, 'type') or node.type is None:
            return False
        return node.type.name == self.node_type

    def filter_node_return_type(self, node):
        if self.node_return_type is None:
            return True
        if not hasattr(node, 'return_type') or node.return_type is None:
            return False
        return node.return_type.name == self.node_return_type

    def passes_filter(self, node):
        return all([
            self.filter_node_class(node),
            self.filter_node_name(node),
            self.filter_node_modifiers(node),
            self.filter_node_annotations(node),
            self.filter_node_extends(node),
            self.filter_node_implements(node),
            self.filter_node_type(node),
            self.filter_node_return_type(node)
        ])

    def get_instances_of(self, ast):
        instances = [node for _, node in ast if self.passes_filter(node)]
        return instances
