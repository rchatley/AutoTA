import sys

from src.project.APIRequest import get_llm_summary
from src.project.ReviewProject import ReviewProject
from src.project.Spec import build_spec

if __name__ == "__main__":
    api_key = None
    if len(sys.argv) < 3:
        repo_dir = 'test/sed_repos/java/SED3'
        spec = build_spec("")

    elif len(sys.argv) < 4:
        repo_dir = sys.argv[1]
        spec_file = sys.argv[2]
        spec = build_spec(spec_file)

    elif len(sys.argv) < 5:
        repo_dir = sys.argv[1]
        spec_file = sys.argv[2]
        api_key = sys.argv[3]
        spec = build_spec(spec_file)

    project = ReviewProject(repo_dir, spec, er_scope='src/main/')
    project.print_feedback()

    if api_key is not None:
        get_llm_summary(project, api_key)
