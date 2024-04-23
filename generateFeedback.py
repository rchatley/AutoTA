import os

from TraversalRule import TraversalRule
from ReviewFile import ReviewFile


def get_task_spec(task_num):
    if task_num == 1:
        return [TraversalRule('identifier', node_type='method', scope=('dir', 'SED3/src/test'),
                              metadata={'pattern': r"^test"}),
                TraversalRule('encapsulation', node_type="class", scope=('file', 'RecentlyUsedList.java'))]


def get_review_files(directory):
    review_files = []

    for root, _, dir_files in os.walk(directory):
        for file_name in dir_files:
            if file_name.endswith('.java'):
                filepath = os.path.join(root, file_name)
                with open(filepath, 'r') as file:
                    source_code = file.read()
                review_files.append(ReviewFile(root, file_name, source_code))

    return review_files


def traverse_files(traversal_files, traversal_rules):
    traversal_feedback = {}

    for review_file in traversal_files:
        file_feedback = []
        for rule in traversal_rules:
            file_feedback += rule.traversal_function(review_file)
        if file_feedback:
            traversal_feedback[review_file] = file_feedback
    return traversal_feedback


if __name__ == "__main__":
    java_source_directory = "SED3"
    task_spec = get_task_spec(1)

    files = get_review_files(java_source_directory)
    feedback = traverse_files(files, task_spec)

    feedback_string = ''
    for problem_files in feedback.keys():
        if feedback[problem_files]:
            feedback_string += problem_files.file_name + '\n'
            feedback_string += '==============' + '\n'
            for line in feedback[problem_files]:
                if line != '':
                    feedback_string += line + '\n'

    print(feedback_string)
