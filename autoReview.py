import sys

from src.project.ExerciseAttempt import ExerciseAttempt
from src.project.Spec import example_template_method_spec

if __name__ == "__main__":
    repo_dir, api_key = None, None
    if len(sys.argv) == 1:
        # Internal Testing
        repo_dir = 'test/example_task/'
    elif len(sys.argv) == 2:
        print("Source directory " + sys.argv[1])
        repo_dir = sys.argv[1]
    elif len(sys.argv) == 3:
        repo_dir = sys.argv[1]
        api_key = sys.argv[2]
    else:
        print("Usage: python autoReview.py [source_directory] [api_key]")
        sys.exit(1)

    spec = example_template_method_spec()

    attempt = ExerciseAttempt(repo_dir, spec)

    # attempt.print_er_graph()

    attempt.perform_analysis()
    attempt.print_feedback()

    if api_key is not None:
        attempt.get_llm_summary(api_key)
        attempt.build_pdf()
