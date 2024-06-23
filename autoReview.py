import sys

from src.project.ReviewProject import ReviewProject
from src.project.Spec import build_spec

if __name__ == "__main__":
    repo_dir, spec_file, api_key = None, None, None
    if len(sys.argv) < 3:
        # Internal Testing
        repo_dir = 'test/example_task/'
        spec = build_spec("")
    elif len(sys.argv) < 4:
        # Command Line
        repo_dir = sys.argv[1]
        spec_file = sys.argv[2]
    elif len(sys.argv) < 5:
        repo_dir = sys.argv[1]
        spec_file = sys.argv[2]
        api_key = sys.argv[3]

    spec = build_spec(spec_file)
    project = ReviewProject(repo_dir, spec, er_scope='main')

    if api_key is not None:
        project.get_llm_summary(api_key)

    if False:
        project.build_pdf()
