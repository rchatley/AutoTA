
class JavaRelations:
    def __init__(self, relation_type):
        self.relation_type = relation_type

    def match(self, node_from, node_to):
        if self.relation_type == 'type':
            if not hasattr(node_from, 'type') or node_from.type is None:
                return False
            if not hasattr(node_from.type, 'name'):
                return False

            return node_from.type.name == node_to.type.name

        if self.relation_type == 'return_type':
            if not hasattr(node_from, 'return_type') or node_from.return_type is None:
                return False
            return node_from.return_type.name == node_to.type.name


