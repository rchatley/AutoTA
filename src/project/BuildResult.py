from enum import Enum


class BuildResult:
    class Result(Enum):
        PASSED = 'Passed'
        COVERAGE = 'Coverage'
        FAILED = 'Failed'
        ERROR = 'Error'

    def __init__(self, result: Result, commit, log):
        self.commit = commit.hexsha[:7]
        self.message = commit.message.strip()
        self.result = result
        self.log = log

    def __str__(self):
        return f"{self.commit} - {self.result} - {self.message} - {self.log}"
