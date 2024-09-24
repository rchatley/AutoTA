from src.project.BuildResult import BuildResult


class BuildResults:
    def __init__(self, summary: str, results: list[BuildResult]):
        self.summary: str = summary
        self.builds: list[BuildResult] = results

    def not_many_commits(self):
        return len(self.builds) < 4

    def mostly_failed(self) -> bool:
        return len([build for build in self.builds if build.passed()]) < len(self.builds) / 2

    def any_failed(self):
        return any(build.failed() for build in self.builds)

    def show_low_coverage(self):
        return any(build.insufficient_coverage() for build in self.builds)

    def all_passed(self):
        return all(build.passed() for build in self.builds)

    def show_style_errors(self):
        return any(build.has_style_errors() for build in self.builds)

    def final_build(self):
        return self.builds[-1]

    def commit_messages(self):
        return [build.message for build in self.builds]
