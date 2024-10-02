import abc
import os

from src.project.Feedback import LineFeedback


class Rule:
    def __init__(self, scope='project'):
        self.scope = scope

    def file_filter(self, file):
        if self.scope == 'project':
            return file.ast

        scope_type, scope = self.scope
        if scope_type == 'dir':
            if file.file_path.startswith(scope):
                return file.ast
            else:
                return None

        if scope_type == 'file':
            if file.file_name == scope:
                return file.ast
            else:
                return None

        print('Invalid scope given')
        return file.ast

    @abc.abstractmethod
    def apply(self, review_file) -> list[LineFeedback]:
        return NotImplementedError
