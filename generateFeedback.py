import os
import re

from javalang import tree, parse


def get_task_spec(task_num):
    if task_num == 3:
        return ["Every field in Class RecentlyUsedList must be encapsulated",
                "Every method in File RecentlyUsedListTest.java must follow name convention",
                "Every invocation of assert in File RecentlyUsedListTest.java must be Library JUnit"]


def get_code(directory):
    java_file_contents = []

    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.java'):
                with open(os.path.join(root, file_name), 'r') as file:
                    source_code = file.read()
                java_file_contents.append(source_code)

    return java_file_contents


def get_asts(source_codes):
    return [parse.parse(source_code) for source_code in source_codes]


def get_function_from_spec(spec_line):
    def rule(ast):
        return [f"({node.position[0]}, {node.position[1]}) | {spec_line}" if
                re.match(r"^test", node.name) else ""
                for path, node in ast.filter(tree.MethodDeclaration)]

    return rule


def get_rules_from_spec(spec_lines):
    return [get_function_from_spec(spec_line) for spec_line in spec_lines]


def traverse_ast(traversal_asts, traversal_rules):
    traversal_feedback = []

    for traversal_ast in traversal_asts:
        for rule in traversal_rules:
            traversal_feedback += rule(traversal_ast)
    return traversal_feedback


if __name__ == "__main__":
    java_source_directory = "SED3"
    task_spec = get_task_spec(3)

    file_contents = get_code(java_source_directory)
    print('- Read file contents')

    asts = get_asts(file_contents)
    print('- Generated AST')

    rules = get_rules_from_spec(task_spec)
    print('- Generated Rules')

    feedback = traverse_ast(asts, rules)
    print('- Basic AST Traversal')

    feedback_string = ''
    for line in feedback:
        if line != '':
            feedback_string += line + '\n'

    print('- Generated Feedback')
    print(feedback_string)
