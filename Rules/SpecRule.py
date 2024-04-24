import os


def default_traversal():
    return ""


def default_filter(_):
    return True


def default_rule(_):
    if not default_filter(_):
        return ""
    return default_traversal()


class SpecRule:

    def __init__(self, scope='project'):
        self.scope = scope
        self.traversal_function = default_traversal

        self.filter = self.build_filter()
        self.traversal = default_traversal

        self.rule = default_rule

    def build_filter(self):
        if self.scope == 'project':
            return default_filter

        scope_type, scope = self.scope
        if scope_type == 'dir':
            def filter_files(review_file):
                root, filename = review_file.root, review_file.file_name
                directory_path = os.path.normpath(scope)
                return os.path.commonpath([os.path.normpath(root), directory_path]) == directory_path

            return filter_files

        if scope_type == 'file':
            def filter_files(review_file):
                return review_file.file_name == scope

            return filter_files

        print('ERROR')
        return default_filter
