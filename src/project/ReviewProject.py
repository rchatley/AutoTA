import os

from src.project.ReviewFile import ReviewFile


def get_pattern_instances(a, b):
    return []


class ReviewProject:

    def __init__(self, directory, language):
        self.directory = directory
        self.language = language
        self.files = []

        lang_ext_dict = {'java': 'java', 'python': 'py'}

        for root, _, dir_files in os.walk(directory):
            for file_name in dir_files:
                if file_name.endswith(f'.{lang_ext_dict[language]}'):
                    self.files.append(ReviewFile(root, file_name))

    def review(self, spec):
        if spec is None:
            return []

        feedback = []

        if spec.rules is not None:
            feedback = self.apply_rules(spec.rules)

        if spec.patterns is not None:
            feedback.extend(self.find_patterns(spec.patterns))

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
            pattern_feedback.extend(get_pattern_instances(pattern, self.files))

        return pattern_feedback
