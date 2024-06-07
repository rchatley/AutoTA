def get_node_name(node, lang):
    if lang == 'java':
        if hasattr(node, 'name'):
            return node.name
        elif hasattr(node, 'declarators'):
            return node.declarators[0].name
    elif lang == 'python':
        if hasattr(node, 'name'):
            return node.name
        if hasattr(node, 'targets'):
            for target in node.targets:
                if hasattr(node, 'id'):
                    return target.id
        if hasattr(node, 'target'):
            if hasattr(node, 'id'):
                return node.target.id


class Filter:
    def __init__(self, language):
        self.language = language

    def get_nodes(self, ast):
        return ast
