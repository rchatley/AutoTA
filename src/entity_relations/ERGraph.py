from src.entity_relations.JavaGraph import build_java_graph
from src.entity_relations.PythonGraph import build_python_graph


class ERGraph:
    def __init__(self, lang, files):
        self.lang = lang
        self.files = files

        if lang == 'java':
            self.graph = build_java_graph(files)
        elif lang == 'python':
            self.graph = build_python_graph(files)
        else:
            self.graph = None
