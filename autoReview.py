import os
import sys

from dotenv import load_dotenv

from src.project.Submission import Submission
from src.project.Spec import camera_exercise_spec

if __name__ == "__main__":

    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY')
    repo_dir = None

    if len(sys.argv) == 2:
        print("Processing directory: " + sys.argv[1])
        repo_dir = sys.argv[1]
    else:
        print("Usage: python autoReview.py [source_directory]")
        sys.exit(1)

    spec = camera_exercise_spec()

    submission = Submission(repo_dir, spec)

    submission.build_each_commit()
    submission.ask_gpt_about_the_commit_messages(api_key)

    submission.perform_analysis(api_key)

    submission.build_pdf()
