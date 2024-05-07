import os

from review_tools.ReviewFile import ReviewFile
from review_tools.ReviewProject import ReviewProject
from review_tools.rules.Design.Strategy import check_for_strategy_pattern
from review_tools.rules.Design.TemplateMethod import check_for_template_method_pattern
from review_tools.rules.Simple.EncapsulationRule import EncapsulationRule
from review_tools.rules.Simple.IndentifierRule import IdentifierRule


def get_task_spec(task_number, task_language):
    java_spec_dict = {1: [EncapsulationRule(), IdentifierRule(node_annotations=['Test'], node_name=r"^test")]}
    python_spec_dict = {1: 'N/A'}
    lang_spec_dict = {'java': java_spec_dict, 'python': python_spec_dict}

    return lang_spec_dict[task_language][task_number]


def get_review_project(task_directory, task_language):
    review_files = []

    for root, _, dir_files in os.walk(task_directory):
        for file_name in dir_files:
            if file_name.endswith(f'.{task_language}'):
                review_files.append(ReviewFile(root, file_name))

    review_project = ReviewProject(task_language, review_files)

    return review_project


if __name__ == "__main__":

    if True:
        task_num = 1
        task_lang = 'java'
        task_dir = f'sample_repos/{task_lang}/SED{task_num}/'

        task_rules = get_task_spec(task_num, task_lang)
        project = get_review_project(task_dir, task_lang)

        for file in project.files:
            for spec in task_rules:
                for instance in spec.rule(file):
                    print(instance)
    elif False:

        task_lang = 'java'
        task_dir = f'sample_repos/{task_lang}/TemplateMethodExample/'

        project = get_review_project(task_dir, task_lang)

        check_for_template_method_pattern(project.files)
    else:

        task_lang = 'java'
        task_dir = f'sample_repos/{task_lang}/StrategyExample/'

        project = get_review_project(task_dir, task_lang)

        check_for_strategy_pattern(project.files)
