import os
from typing import List

from src.entity_relations import JavaGraph
from src.entity_relations.JavaGraph import build_code_graph, print_graph
from src.project.JavaFile import JavaFile
from src.project.Spec import Spec
from src.project.utils import create_feedback_pdf, gpt_api_request
from src.rules.EncapsulationRule import EncapsulationRule
from src.rules.IdentifierRule import IdentifierRule


def gather_files_from(directory, file_extension) -> list[JavaFile]:
    files = []
    for root, _, dir_files in os.walk(directory):
        for file_name in dir_files:
            if file_name.endswith(f'.{file_extension}'):
                files.append(JavaFile(root, os.path.relpath(root, directory), file_name))
    return files


class ExerciseAttempt:
    spec: Spec
    files: list[JavaFile]
    er_graph: JavaGraph

    def __init__(self, directory, spec: Spec, scope_restriction: str = None):
        self.directory = directory
        self.files = gather_files_from(directory, "java")
        self.spec = spec

        self.er_graph = self.build_graph_of_code(scope_restriction)

        self.summary = ""
        self.feedback = None

    def build_graph_of_code(self, scope_restriction) -> JavaGraph:
        if scope_restriction is None:
            return build_code_graph(self.files)
        else:
            return build_code_graph(self._files_within(scope_restriction))

    def perform_analysis(self):
        feedback = []
        if self.spec.rules is not None:
            feedback = self.apply_rules()
        if self.spec.structures is not None:
            feedback.extend(self.find_structures())

        self.feedback = feedback

    def apply_rules(self):
        complete_feedback = ["CODE STYLE RULES:"]
        for rule in self.spec.rules:
            complete_feedback.append(str(rule) + ':')
            rule_feedback = []
            for file in self.files:
                feedback = rule.apply(file)
                if feedback:
                    file.feedback.extend(feedback)
                    rule_feedback.extend(
                        [f'File: {file.file_name}, Line: {line}: {text}' for
                         line, text in feedback])
            if not rule_feedback:
                if isinstance(rule, EncapsulationRule):
                    complete_feedback.append(
                        f'All classes within {rule.scope} were properly encapsulated')
                elif isinstance(rule, IdentifierRule):
                    complete_feedback.append(
                        f'All {rule.node_filter.node_class}s within {rule.scope} had the correct identifier format of {rule.node_filter.node_name}')
            else:
                complete_feedback.extend(rule_feedback)
        complete_feedback.append("")
        return complete_feedback

    def find_structures(self):
        structure_feedback = ["EXPECTED STRUCTURES:"]
        for structure in self.spec.structures:
            structure_feedback.append('-' + structure.name + '\n' +
                                      structure.find_potential_isomorphisms(self.er_graph))
        return structure_feedback

    def print_er_graph(self):
        print_graph(self.er_graph['entities'], self.er_graph['relations'])

    def print_feedback(self):
        if not self.feedback:
            print('User code passes all rules')
        else:
            for feedback in self.feedback:
                print(feedback)

    def get_llm_summary(self, api_key):
        self.summary = gpt_api_request(self.files, self.feedback, api_key)

    def build_pdf(self):
        create_feedback_pdf(self.files, self.spec.task, self.summary + "\n\n" + "\n".join(self.feedback),
                            self.directory)

    def _files_within(self, scope_restriction) -> list[JavaFile]:
        scope_dir = os.path.normpath(scope_restriction)
        scoped_files = [file for file in self.files if
                        os.path.commonpath([os.path.normpath(file.relative_path), scope_dir]) == scope_dir]
        return scoped_files
