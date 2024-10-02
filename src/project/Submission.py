import os
import subprocess


from git import Repo
from openai import OpenAI
from pydantic import BaseModel

from src.entity_relations import JavaGraph
from src.entity_relations.CodeStructure import SearchResult
from src.entity_relations.JavaGraph import build_code_graph, print_graph
from src.project.BuildResult import BuildResult
from src.project.BuildResults import BuildResults
from src.project.Feedback import FileFeedback
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

    # Remove files that are not present on the disk
    changed_files = {file for file in changed_files if os.path.exists(os.path.join(repo_path, file))}

    return changed_files


def run_gradle_build_for_each_commit(repo_path: str) -> BuildResults:
    summary: str = ""
    build_results: list[BuildResult] = []

    try:
        # Open the repository
        repo = Repo(repo_path)

        # Ensure the repository is valid
        if repo.bare:
            summary = "The repository is bare, cannot process."
        else:

            # Get all commits, starting from the most recent one
            commits = list(repo.iter_commits(reverse=True))

            # Print the commit messages, skipping the initial commit
            summary = f"You made {len(commits) - 1} commits:"

            for commit in commits[1:]:  # Skip the initial commit
                build_results.append(run_the_build(commit, repo, repo_path))

    except Exception as e:
        print(f"An error occurred: {e}")

    return BuildResults(summary, build_results)


def run_the_build(commit, repo, repo_path) -> BuildResult:
    # Checkout the commit
    repo.git.reset(commit.hexsha, hard=True)
    # Run the tests using gradlew
    gradlew_path = os.path.join(repo_path, './gradlew')

    try:
        result, stdout_log = run_gradle("clean", gradlew_path, repo_path)

        if result.returncode != 0:
            print(f"An error occurred while cleaning the project: {result.stderr}")
            return BuildResult(BuildResult.Status.ERROR, commit, result.stderr.strip())

        result, stdout_log = run_gradle("test", gradlew_path, repo_path)

        if result.returncode == 0:
            print(f"Tests passed for commit {commit.hexsha}.")
        else:
            print(f"Tests failed for commit {commit.hexsha}.")
            return BuildResult(BuildResult.Status.FAILED, commit, result.stderr.strip())

        result, stdout_log = run_gradle("check", gradlew_path, repo_path)

        if "Execution failed for task ':jacocoTestCoverageVerification'" in result.stderr:
            print(f"Coverage check failed for commit {commit.hexsha}.")
            return BuildResult(BuildResult.Status.COVERAGE, commit, stdout_log)
        elif "Execution failed for task ':checkstyleTest'" in result.stderr:
            print(f"Code style check failed for commit {commit.hexsha}.")
            return BuildResult(BuildResult.Status.STYLE, commit, stdout_log)
        else:
            print(f"Build passed for commit {commit.hexsha}.")
            return BuildResult(BuildResult.Status.PASSED, commit, stdout_log)

    except Exception as e:
        print(f"An error occurred while testing commit {commit.hexsha}: {str(e)}")
        return BuildResult(BuildResult.Status.ERROR, commit, stdout_log)


def run_gradle(task, gradlew_path, repo_path):
    result = subprocess.run(
        [gradlew_path, task], cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout_log = result.stdout.strip()
    return result, stdout_log


def failed(result):
    return result.status == BuildResult.Status.FAILED


class Submission:
    spec: Spec
    edited_files: list[JavaFile]
    additional_types: list[JavaFile]
    er_graph: JavaGraph
    comments: list[str]

    def __init__(self, directory, spec: Spec, scope_restriction: str = None):

        self.directory = directory
        self.spec = spec
        self.edited_files = [JavaFile(directory, f) for f in list_edited_files(directory) if f.endswith('.java')]
        self.additional_types = [JavaFile(directory, f) for f in spec.additional_files if f.endswith('.java')]
        self.all_files = self.edited_files + self.additional_types

        self.er_graph = self.build_graph_of_code(scope_restriction)

        self.summary = ""
        self.build_results: BuildResults = None
        self.rules_feedback = None
        self.structure_feedback = None
        self.gpt_feedback = None
        self.comments = []

    def build_graph_of_code(self, scope_restriction) -> JavaGraph:
        if scope_restriction is None:
            return build_code_graph(self.all_files)
        else:
            return build_code_graph(self._files_within(scope_restriction))

    def perform_analysis(self, api_key):
        self.rules_feedback = []
        self.structure_feedback = []
        if self.spec.rules is not None:
            self.rules_feedback = self.apply_rules()
        # if self.spec.structures is not None:
        #     self.structure_feedback = self.find_structures()
        if self.spec.marking_points is not None:
            self.ask_gpt(api_key)

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
                        f'All {rule.node_filter.node_class}s within {rule.scope} had the correct identifier '
                        f'format of {rule.node_filter.node_name}')
            else:
                complete_feedback.extend(rule_feedback)
        complete_feedback.append("")
        return complete_feedback

    def ask_gpt(self, api_key):
        client = OpenAI(api_key=api_key)

        for file in self.edited_files:
            feedback_points = self.spec.marking_points_for_file(file.file_name)

            if feedback_points is not None:

                ta_prompt = (
                    f"Here is part of the Java code written by a student as a solution to an assignment:\n\n{file.contents_with_line_numbers()}\n\n"
                    f"Here is a description of what we are looking for in this assignment:\n\n{self.spec.overview}\n\n"
                    f"Your job is to give feedback to the student."
                    f"Given this context, make comments on the code, particularly about the following:\n")

                for i, marking_point in enumerate(feedback_points, 1):
                    ta_prompt += f"- {marking_point}\n"

                response = client.beta.chat.completions.parse(
                    model="gpt-4o-2024-08-06",
                    messages=[
                      {"role": "system",
                       "content": "You are an expert Java programmer acting as a "
                                  "teaching assistant for a university course on "
                                  "software design. Your character is to be kind"
                                  "and fair, while still being critical."
                      },
                      {"role": "user", "content": ta_prompt}],
                    response_format=FileFeedback)

                line_by_line_feedback = response.choices[0].message.parsed.line_feedback
                file.feedback.extend(line_by_line_feedback)

                # for line_feedback in line_by_line_feedback:
                #     print(f"File: {file.file_name}, Line: {line_feedback.line}: {line_feedback.feedback}")

    def find_structures(self):
        structure_feedback = []
        for structure in self.spec.structures:
            result = structure.find_potential_isomorphisms(self.er_graph)
            if result == SearchResult.FOUND:
                structure_feedback.append(f'{structure.name}: {structure.description} - GOOD')
            elif result == SearchResult.CLOSE:
                structure_feedback.append(f'{structure.name}: Close, the idea was that the {structure.description}')
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
                            self.build_results, commit_msg_opinion=self.comments, name="SED")

    def _feedback(self):
        return self.summary + "\n\n" + "\n".join(self.structure_feedback)

    def _files_within(self, scope_restriction) -> list[JavaFile]:
        scope_dir = os.path.normpath(scope_restriction)
        scoped_files = [file for file in self.all_files if
                        os.path.commonpath([os.path.normpath(file.relative_path), scope_dir]) == scope_dir]
        return scoped_files

    def build_each_commit(self):
        self.build_results = run_gradle_build_for_each_commit(self.directory)

    def ask_gpt_about_the_commit_messages(self, api_key):
        client = OpenAI(api_key=api_key)

        prompt = (
            f"Here are some commit messages written by a student. "
            f"Can you give me a one-sentence opinion on the quality of these commit messages?.\n\n")

        prompt += ("\n".join(self.build_results.commit_messages()))

        response = client.chat.completions.create(model="gpt-4o",
                                                  messages=[
                                                      {"role": "system",
                                                       "content": "You are an expert Java programmer acting as a teaching assistant for a university course on software design. Your character is to be critical but fair."},
                                                      {"role": "user", "content": prompt}
                                                  ])

        opinion = response.choices[0].message.content

        print(f"Opinion on commit messages: {opinion}")

        self.comments.append(opinion)
