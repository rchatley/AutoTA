import os


def default_filter(file):
    return file.ast


def default_traversal(_):
    return []


def default_rule(_):
    if not default_filter(_):
        return ""
    return default_traversal(_)


def build_filter(scope):
    if scope == 'project':
        return default_filter

    scope_type, scope = scope
    if scope_type == 'dir':
        def filter_files(review_file):
            root, filename = review_file.root, review_file.file_name
            directory_path = os.path.normpath(scope)
            if os.path.commonpath(
                    [os.path.normpath(root), directory_path]) == directory_path:
                return review_file.ast
            else:
                return None

        return filter_files

    if scope_type == 'file':
        def filter_files(review_file):
            if review_file.file_name == scope:
                return review_file.ast
            else:
                return None

        return filter_files

    print('ERROR')
    return default_filter


class SimpleRule:
    def __init__(self, scope='project'):
        self.filter = build_filter(scope)
        self.traversal = default_traversal

        self.rule = default_rule

    def build_rule(self):
        def rule(review_file):
            filtered_ast = self.filter(review_file)
            if filtered_ast is None:
                return []

            return self.traversal(filtered_ast)

        return rule
