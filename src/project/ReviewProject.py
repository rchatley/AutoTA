import os

from src.project.ReviewFile import ReviewFile


class ReviewProject:

    def __init__(self, directory, spec, uml_scope=None):
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

        # BUILD UML GRAPH
        self.uml_graph = uml_scope

        # GET FEEDBACK
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
        if rules is None:
            return []

        rule_feedback = []
        for file in self.files:
            for rule in rules:
                feedback = rule.apply(file)
                if feedback:
                    rule_feedback.extend(feedback)

        return rule_feedback

    def find_patterns(self, patterns):
        if patterns is None:
            return []

        pattern_feedback = []
        for pattern in patterns:
            feedback = pattern.find_in(self.uml_graph)
            if feedback:
                pattern_feedback.extend(feedback)

        return pattern_feedback

    def get_summary(self, api_key_file):
        return api_key_file
