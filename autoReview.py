import sys

from review.filters.JavaFilter import JavaFilter
from review.patterns.DesignPattern import DesignPattern
from review.project.ReviewProject import ReviewProject
from review.project.Spec import get_task_spec
from review.rules.IdentifierRule import IdentifierRule

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

                project = ReviewProject(task_dir, task_lang)

                # for file in project.files:
                #     for rule in task_rules:
                #         print(rule.rule(file))

        task_dir = 'sed_repos/java/SED4/'
        project = ReviewProject(task_dir, 'java')

        print(DesignPattern('singleton').find_pattern(project))

        project.apply_rules(
            [IdentifierRule(node_filter=JavaFilter(node_class='method',
                                                   node_annotations=[
                                                       'Test'],
                                                   node_name=r"^test"))])

    elif len(sys.argv) < 3:
        repo_dir = sys.argv[1]
        spec_file = sys.argv[2]

        project = ReviewProject(repo_dir, sys.argv[1])
