def get_node_name(node, lang):
    if lang == 'java':
        if hasattr(node, 'name'):
            return node.name
        elif hasattr(node, 'declarators'):
            return node.declarators[0].name
    elif lang == 'python':
        return node.name


class Filter:
    def __init__(self, language):
        self.language = language

    def get_nodes(self, ast):
        return ast
