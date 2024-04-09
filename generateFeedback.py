import os
import re

from javalang import tree

from ReviewFile import ReviewFile


def get_task_spec(task_num):
    if task_num == 3:
        return [("Every method in File RecentlyUsedListTest.java must follow name convention", 'IDENTIFIER', 'METHOD',
                 '@Test', r"^test"),
                ("Every field in Class RecentlyUsedList must be encapsulated", 'ENCAPSULATION')]


def get_review_files(directory):
    review_files = []

    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.java'):
                filepath = os.path.join(root, file_name)
                with open(filepath, 'r') as file:
                    source_code = file.read()
                review_files.append(ReviewFile(filepath, source_code))

    return review_files


def get_function_from_spec(spec_line):
    rule_text = spec_line[0]
    rule_type = spec_line[1]

    if rule_type == 'IDENTIFIER':

        rule_scope = spec_line[2]
        if rule_scope == 'METHOD':
            class_name = tree.MethodDeclaration

        rule_pattern = spec_line[4]

        def rule(ast):
            return [f"({node.position[0]}, {node.position[1]}) | {rule_text}" if
                    re.match(rule_pattern, node.name) else ""
                    for path, node in ast.filter(class_name)]

    elif rule_type == 'ENCAPSULATION':
        def rule(ast):
            errors = []
            class_scope = [node for path, node in ast.filter(tree.ClassDeclaration)]
            for class_dec in class_scope:
                # print(class_dec)
                for field_decl in class_dec.fields:
                    # print(field_decl)
                    if 'private' not in field_decl.modifiers:
                        errors.append(f"({field_decl.position[0]}, {field_decl.position[1]}) | {rule_text}")
            return errors
    else:
        def rule(ast):
            return []

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

    files = get_review_files(java_source_directory)
    print('- Generated Review Files')

    rules = get_rules_from_spec(task_spec)
    print('- Generated Rules')

    feedback = traverse_ast([file.ast for file in files], rules)
    print('- Basic AST Traversal')

    feedback_string = ''
    for line in feedback:
        if line != '':
            feedback_string += line + '\n'

    print('- Generated Feedback')
    print(feedback_string)
