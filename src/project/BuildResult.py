from enum import Enum


class BuildResult:
    class Status(Enum):
        STYLE = 'Style'
        PASSED = 'Passed'
        COVERAGE = 'Coverage'
        FAILED = 'Failed'
        ERROR = 'Error'

    def __init__(self, status: Status, commit, log):
        self.commit = commit.hexsha[:7]
        self.message = commit.message.strip()
        self.status = status
        self.log = log

    def __str__(self):
        return f"{self.commit} - {self.status} - {self.message} - {self.log}"

    def failed(self) -> bool:
        return self.status == BuildResult.Status.FAILED

    def insufficient_coverage(self) -> bool:
        return self.status == BuildResult.Status.COVERAGE

    def bad_style(self) -> bool:
        return self.status == BuildResult.Status.STYLE

    def passed(self) -> bool:
        return self.status == BuildResult.Status.PASSED

    def has_style_errors(self) -> bool:
        return self.status == BuildResult.Status.STYLE
