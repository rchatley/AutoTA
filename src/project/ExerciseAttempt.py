import os

from git import Repo

from src.entity_relations import JavaGraph
from src.entity_relations.CodeStructure import SearchResult
from src.entity_relations.JavaGraph import build_code_graph, print_graph
from src.project.JavaFile import JavaFile
from src.project.Spec import Spec
from src.project.utils import create_feedback_pdf, gpt_api_request
from src.rules.EncapsulationRule import EncapsulationRule
from src.rules.IdentifierRule import IdentifierRule


def list_edited_files(repo_path) -> set[str]:
    # Open the repository
    repo = Repo(repo_path)

    # Ensure the repository is valid
    if repo.bare:
        print("The repository is bare, cannot process.")
        return set()

    # Get all commits
    commits = list(repo.iter_commits())

    # Get the first commit
    first_commit = commits[-1]

    # Initialize a set to store the changed files
    changed_files = set()

    # Iterate over all commits from the first to the head
    for commit in commits:
        if commit == first_commit:
            break
        for diff in commit.diff(commit.parents or None):
            changed_files.add(diff.a_path)
            if diff.b_path:
                changed_files.add(diff.b_path)

    # Get uncommitted changes
    uncommitted_changes = repo.index.diff(None)

    # Add uncommitted changes to the set
    for diff in uncommitted_changes:
        changed_files.add(diff.a_path)
        if diff.b_path:
            changed_files.add(diff.b_path)

    # Add untracked files to the set
    untracked_files = repo.untracked_files
    changed_files.update(untracked_files)

    return changed_files


def commit_log(repo_path):
    output = []

    try:
        # Open the repository
        repo = Repo(repo_path)

        # Ensure the repository is valid
        if repo.bare:
            output.append("The repository is bare, cannot process.")
            return

        # Get all commits, starting from the most recent one
        commits = list(repo.iter_commits(reverse=True))

        # Print the commit messages, skipping the initial commit
        output.append(f"You made {len(commits) - 1} commits:")
        for commit in commits[1:]:  # Skip the last commit, which is the initial one
            output.append(f" - {commit.hexsha[:7]}: {commit.message.strip()}")

    except Exception as e:
        print(f"An error occurred: {e}")

    return "\n".join(output)


class ExerciseAttempt:
    spec: Spec
    edited_files: list[JavaFile]
    additional_types: list[JavaFile]
    er_graph: JavaGraph

    def __init__(self, directory, spec: Spec, scope_restriction: str = None):

        self.directory = directory
        self.spec = spec
        self.edited_files = [JavaFile(directory, f) for f in list_edited_files(directory) if f.endswith('.java')]
        self.additional_types = [JavaFile(directory, f) for f in spec.additional_files if f.endswith('.java')]
        self.all_files = self.edited_files + self.additional_types

        self.er_graph = self.build_graph_of_code(scope_restriction)

        self.summary = ""
        self.rules_feedback = None
        self.structure_feedback = None

    def build_graph_of_code(self, scope_restriction) -> JavaGraph:
        if scope_restriction is None:
            return build_code_graph(self.all_files)
        else:
            return build_code_graph(self._files_within(scope_restriction))

    def perform_analysis(self):
        self.rules_feedback = []
        self.structure_feedback = []
        if self.spec.rules is not None:
            self.rules_feedback = self.apply_rules()
        if self.spec.structures is not None:
            self.structure_feedback = self.find_structures()

    def apply_rules(self):
        complete_feedback = ["CODE STYLE RULES:"]
        for rule in self.spec.rules:
            complete_feedback.append(str(rule) + ':')
            rule_feedback = []
            for file in self.edited_files:
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
        structure_feedback = []
        for structure in self.spec.structures:
            result = structure.find_potential_isomorphisms(self.er_graph)
            if result == SearchResult.FOUND:
                structure_feedback.append(f'{structure.name}: {structure.description} - GOOD')
            elif result == SearchResult.CLOSE:
                structure_feedback.append(f'{structure.name}: Close, that idea was that the {structure.description}')
            else:
                structure_feedback.append(f'{structure.name}: '
                                          f'This does not match the expected structure. The {structure.description}')

        return structure_feedback

    def print_er_graph(self):
        print_graph(self.er_graph['entities'], self.er_graph['relations'])

    def get_llm_summary(self, api_key):
        self.summary = gpt_api_request(self.edited_files, self.structure_feedback, api_key)

    def build_pdf(self):
        create_feedback_pdf(self.edited_files, self.spec.task,
                            commit_log(self.directory), "\n".join(self.structure_feedback), "SED")

    def _feedback(self):
        return self.summary + "\n\n" + "\n".join(self.structure_feedback)

    def _files_within(self, scope_restriction) -> list[JavaFile]:
        scope_dir = os.path.normpath(scope_restriction)
        scoped_files = [file for file in self.all_files if
                        os.path.commonpath([os.path.normpath(file.relative_path), scope_dir]) == scope_dir]
        return scoped_files
