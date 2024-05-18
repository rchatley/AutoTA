import re
from typing import List, Optional, Union, Any
from javalang import tree

class_map = {
    'node': tree.Node,
    'class': tree.ClassDeclaration,
    'method': tree.MethodDeclaration,
    'method_invocation': tree.MethodInvocation,
    'field': tree.FieldDeclaration,
    'constructor': tree.ConstructorDeclaration,
    'interface': tree.InterfaceDeclaration
}


class JavaFilter:
    def __init__(
            self,
            node_class: str = 'node',
            node_name: Optional[str] = None,
            node_modifiers: Optional[List[str]] = None,
            node_annotations: Optional[List[str]] = None,
            node_extends: Optional[str] = None,
            node_implements: Optional[List[str]] = None,
            node_type: Optional[str] = None,
            node_return_type: Optional[str] = None
    ) -> None:
        self.node_class = node_class
        self.node_name = node_name
        self.node_modifiers = node_modifiers or []
        self.node_annotations = node_annotations or []
        self.node_extends = node_extends
        self.node_implements = node_implements or []
        self.node_type = node_type
        self.node_return_type = node_return_type

    def get_instances_of(self, ast: List[Union[tree.Node, Any]]) -> List[tree.Node]:
        return [node for _, node in ast if self.passes_filter(node)]

    def passes_filter(self, node: tree.Node) -> bool:
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

    def filter_node_class(self, node: tree.Node) -> bool:
        return isinstance(node, class_map[self.node_class])

    def filter_node_name(self, node: tree.Node) -> bool:
        if self.node_name is None:
            return True

        comp_name = getattr(node, 'name', None)
        if comp_name is None and hasattr(node, 'declarators'):
            comp_name = node.declarators[0].name

        return bool(comp_name and re.match(self.node_name, comp_name))

    def filter_node_modifiers(self, node: tree.Node) -> bool:
        if not self.node_modifiers:
            return True

        node_modifiers = getattr(node, 'modifiers', None)
        return bool(node_modifiers and set(self.node_modifiers).issubset(
            set(node_modifiers)))

    def filter_node_annotations(self, node: tree.Node) -> bool:
        if not self.node_annotations:
            return True

        node_annotations = getattr(node, 'annotations', None)
        if node_annotations is None:
            return False

        annotation_names = [annotation.name for annotation in node_annotations]
        return set(self.node_annotations).issubset(set(annotation_names))

    def filter_node_extends(self, node: tree.Node) -> bool:
        if self.node_extends is None:
            return True

        node_extends = getattr(node, 'extends', None)
        return bool(node_extends and node_extends.name == self.node_extends)

    def filter_node_implements(self, node: tree.Node) -> bool:
        if not self.node_implements:
            return True

        node_implements = getattr(node, 'implements', None)
        if not node_implements:
            return False

        implements_names = [implements.name for implements in node_implements]
        return set(self.node_implements).issubset(set(implements_names))

    def filter_node_type(self, node: tree.Node) -> bool:
        if self.node_type is None:
            return True

        node_type = getattr(node, 'type', None)
        return bool(node_type and node_type.name == self.node_type)

    def filter_node_return_type(self, node: tree.Node) -> bool:
        if self.node_return_type is None:
            return True

        node_return_type = getattr(node, 'return_type', None)
        return bool(
            node_return_type and node_return_type.name == self.node_return_type)
