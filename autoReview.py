import sys

from src.project.ReviewProject import ReviewProject
from src.project.Spec import build_spec

if __name__ == "__main__":
    if len(sys.argv) < 2:
        directory = 'test/sed_repos/java/SED1'
        spec = build_spec("")
        project = ReviewProject(directory, spec)

        project.print_feedback()

    elif len(sys.argv) < 3:
        repo_dir = sys.argv[1]
        spec_file = sys.argv[2]

        spec = build_spec(spec_file)
        project = ReviewProject(repo_dir, spec)

        project.print_feedback()

        # print(project.get_summary(key_file))
