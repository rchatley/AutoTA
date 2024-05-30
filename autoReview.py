import os
import sys

from review.patterns.DesignPattern import find_pattern
from review.project.ReviewFile import ReviewFile
from review.project.ReviewProject import ReviewProject
from review.rules.EncapsulationRule import EncapsulationRule
from review.rules.IndentifierRule import IdentifierRule


def get_task_spec(task_number, task_language):
    java_spec_dict = {1: [EncapsulationRule(),
                          IdentifierRule(annotations=['Test'],
                                         name_format=r"^test")],
                      3: None,
                      4: None,
                      7: None}
    python_spec_dict = {1: None,
                        3: None,
                        4: None,
                        7: None}
    lang_spec_dict = {'java': java_spec_dict, 'python': python_spec_dict}

    return lang_spec_dict[task_language][task_number]


def get_review_project(task_directory, task_language):
    review_files = []
    lang_ext_dict = {'java': 'java', 'python': 'py'}

    for root, _, dir_files in os.walk(task_directory):
        for file_name in dir_files:
            if file_name.endswith(f'.{lang_ext_dict[task_language]}'):
                review_files.append(ReviewFile(root, file_name))

    review_project = ReviewProject(task_language, review_files)

    return review_project


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sed_tasks = [1, 3, 4, 7]
        task_langs = ['java', 'python']

        for task_num in sed_tasks:
            for task_lang in task_langs:
                task_dir = f'sed_repos/{task_lang}/SED{task_num}/'

                task_rules = get_task_spec(task_num, task_lang)

                if task_rules is None:
                    continue

                project = get_review_project(task_dir, task_lang)

                # for file in project.files:
                #     for rule in task_rules:
                #         print(rule.rule(file))

        task_dir = 'sed_repos/java/SED4/'
        project = get_review_project(task_dir, 'java')

        print(find_pattern('singleton', project))

    elif len(sys.argv) < 3:
        repo_dir = sys.argv[1]
        spec_file = sys.argv[2]

        project = get_review_project(repo_dir, sys.argv[1])
