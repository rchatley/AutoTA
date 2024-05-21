import os

from review_tools.ReviewFile import ReviewFile
from review_tools.ReviewProject import ReviewProject
from review_tools.rules import DesignPattern
from review_tools.rules.Simple.EncapsulationRule import EncapsulationRule
from review_tools.rules.Simple.IndentifierRule import IdentifierRule


def get_task_spec(task_number, task_language):
    java_spec_dict = {1: [EncapsulationRule(),
                          IdentifierRule(node_annotations=['Test'],
                                         node_name=r"^test")]}
    python_spec_dict = {1: 'N/A'}
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

    if False:
        task_lang = 'python'
        task_num = sed_tasks[0]

        task_dir = f'sed_repos/{task_lang}/SED{task_num}/'

        task_rules = get_task_spec(task_num, task_lang)
        project = get_review_project(task_dir, task_lang)

        for file in project.files:
            print(file.ast)
            get_instances_of(file.ast, 'class')
    elif False:

        task_lang = 'java'
        task_dir = f'sample_repos/{task_lang}/SED/4/'

        project = get_review_project(task_dir, task_lang)

        print(DesignPattern.find_pattern('singleton', project))

    elif True:

        task_lang = 'java'
        task_dir = f'sed_repos/{task_lang}/SED3/'

        project = get_review_project(task_dir, task_lang)

        print(DesignPattern.find_pattern('template', project))
    else:

        task_lang = 'java'
        task_dir = f'sample_repos/{task_lang}/StrategyExample/'

        project = get_review_project(task_dir, task_lang)

        DesignPattern.find_pattern('strategy', project)
