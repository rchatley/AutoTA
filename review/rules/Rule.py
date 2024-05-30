import os


def default_filter(file):
    return file.ast


def build_filter(scope):
    if scope == 'project':
        return default_filter

    scope_type, scope = scope
    if scope_type == 'dir':
        def filter_files(review_file):
            directory_path = os.path.normpath(scope)
            if os.path.commonpath(
                    [os.path.normpath(review_file.root),
                     directory_path]) == directory_path:
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


class Rule:
    def __init__(self, scope='project'):
        self.filter = build_filter(scope)

    def apply(self, review_file):
        return []
