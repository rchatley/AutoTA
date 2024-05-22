import os

from review_tools.project.ReviewFile import ReviewFile
from review_tools.project.ReviewProject import ReviewProject
from review_tools.rules.DesignPattern import find_pattern
from review_tools.rules.simple_rules.EncapsulationRule import EncapsulationRule
from review_tools.rules.simple_rules.IndentifierRule import IdentifierRule


def get_task_spec(task_number, task_language):
    java_spec_dict = {1: [EncapsulationRule(),
                          IdentifierRule(annotations=['Test'],
                                         node_name=r"^test")],
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

    task_dir = f'tests/test_repos/java/Strategy'
    project = get_review_project(task_dir, 'java')

    print(find_pattern('strategy', project))
