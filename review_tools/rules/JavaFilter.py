import re

from javalang import tree

class_map = {'node': tree.Node,
             'class': tree.ClassDeclaration,
             'method': tree.MethodDeclaration,
             'method_invocation': tree.MethodInvocation,
             'field': tree.FieldDeclaration,
             'constructor': tree.ConstructorDeclaration,
             'interface': tree.InterfaceDeclaration}


def filter_node_name(node, node_name):
    if node_name is None:
        return True

    if not hasattr(node, 'name'):
        if hasattr(node, 'declarators'):
            comp_name = node.declarators[0].name
        else:
            return False
    else:
        comp_name = node.name

    return re.match(node_name, comp_name)


def filter_node_modifiers(node, node_modifiers):
    if node_modifiers is None or len(node_modifiers) == 0:
        return True

    if not hasattr(node, 'modifiers'):
        return False

    return set(node_modifiers).issubset(set(node.modifiers))


def filter_node_annotations(node, node_annotations):
    if node_annotations is None or len(node_annotations) == 0:
        return True

    if not hasattr(node, 'annotations'):
        return False

    annotation_names = [annotation.name for annotation in node.annotations]

    return set(node_annotations).issubset(set(annotation_names))


def filter_node_extends(node, node_extends):
    if node_extends is None:
        return True

    if not hasattr(node, 'extends'):
        return False

    return node.extends and node.extends.name == node_extends


def filter_node_implements(node, node_implements):
    if node_implements is None or len(node_implements) == 0:
        return True

    if not hasattr(node, 'implements') or not node.implements:
        return False

    implements_names = [implements.name for implements in node.implements]

    return set(node_implements).issubset(set(implements_names))


def filter_node_type(node, node_type):
    if node_type is None:
        return True

    if not hasattr(node, 'type') or node.type is None:
        return False

    return node.type.name == node_type


def filter_node_return_type(node, node_return_type):
    if node_return_type is None:
        return True

    if not hasattr(node, 'return_type') or node.return_type is None:
        return False

    return node.return_type.name == node_return_type


def passes_filter(node, node_class, node_name, node_modifiers,
                  node_annotations,
                  node_extends, node_implements, node_type, node_return_type):
    return (isinstance(node, class_map[node_class]) and
            filter_node_name(node, node_name) and
            filter_node_modifiers(node, node_modifiers) and
            filter_node_annotations(node, node_annotations) and
            filter_node_extends(node, node_extends) and
            filter_node_implements(node, node_implements) and
            filter_node_type(node, node_type) and
            filter_node_return_type(node, node_return_type))


def get_instances_of(ast, node_class='node', node_name=None,
                     node_modifiers=None, node_annotations=None,
                     node_extends=None, node_implements=None, node_type=None,
                     node_return_type=None):
    instances = [node for _, node in ast if
                 passes_filter(node, node_class, node_name, node_modifiers,
                               node_annotations, node_extends,
                               node_implements, node_type, node_return_type)]

    return instances
