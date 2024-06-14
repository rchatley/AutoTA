import os

from src.entity_relations.JavaGraph import build_java_graph
from src.entity_relations.PythonGraph import build_python_graph
from src.project.ReviewFile import ReviewFile
from src.rules.EncapsulationRule import EncapsulationRule
from src.rules.IdentifierRule import IdentifierRule


class ReviewProject:

    def __init__(self, directory, spec, er_scope=None):
        self.directory = directory
        self.spec = spec
        self.files = []

        lang_ext_dict = {'java': 'java', 'python': 'py'}
        file_extension = lang_ext_dict[spec.language]

        for root, _, dir_files in os.walk(directory):
            for file_name in dir_files:
                if file_name.endswith(f'.{file_extension}'):
                    self.files.append(
                        ReviewFile(root, os.path.relpath(root, directory),
                                   file_name))

        if er_scope is None:
            self.er_graph = self.build_er_graph(self.files)
        else:
            scope_dir = os.path.normpath(er_scope)
            scoped_files = [file for file in self.files if
                            os.path.commonpath(
                                [os.path.normpath(file.relative_path),
                                 scope_dir]) == scope_dir]
            self.er_graph = self.build_er_graph(scoped_files)

        self.feedback = self.get_feedback()

    def get_feedback(self):
        if self.spec is None:
            return []
        feedback = []
        if self.spec.rules is not None:
            feedback = self.apply_rules(self.spec.rules)
        if self.spec.patterns is not None:
            feedback.extend(self.find_patterns(self.spec.patterns))

        return feedback

    def apply_rules(self, rules):
        rule_feedback = []
        for file in self.files:
            for rule in rules:
                feedback = rule.apply(file)
                if feedback:
                    rule_feedback.extend(feedback)
                else:
                    if isinstance(rule, EncapsulationRule):
                        rule_feedback.append(
                            f'All classes within file {file.file_name} within {rule.scope} were encapsulated')
                    elif isinstance(rule, IdentifierRule):
                        rule_feedback.append(
                            f'All {rule.node_filter.node_class}s within file {file.file_name} within {rule.scope} had the correct identifier format of  {rule.node_filter.node_name}')

        return rule_feedback

    def find_patterns(self, patterns):
        pattern_feedback = []
        for pattern in patterns:
            feedback = pattern.find_potential_isomorphisms(self.er_graph)
            pattern_feedback.append(feedback)

        return pattern_feedback

    def build_er_graph(self, files):
        if self.spec.language == 'java':
            return build_java_graph(files)
        elif self.spec.language == 'python':
            return build_python_graph(files)

    def print_feedback(self):
        if not self.feedback:
            print('User code passes all rules')
        else:
            for feedback in self.feedback:
                print(feedback)
