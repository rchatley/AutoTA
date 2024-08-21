import os
import sys

from src.project.ExerciseAttempt import ExerciseAttempt
from src.project.Spec import example_template_method_spec, camera_exercise_spec

from dotenv import load_dotenv

if __name__ == "__main__":

    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY')
    repo_dir = None

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

    spec = camera_exercise_spec()

    attempt = ExerciseAttempt(repo_dir, spec)

    # attempt.print_er_graph()

    attempt.perform_analysis(api_key)

    attempt.build_pdf()
