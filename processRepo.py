import sys

import openai

openai.api_key = "SECRET"


def compose_api_request(repo_path):
    # GET DATA FROM REPO

    # GET RULES

    # BUILD REQUEST


    client = openai.OpenAI()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(0)
    else:
        repo_path = sys.argv[1]

    compose_api_request(repo_path)
    # SEND REQUEST

    # PROCESS RESPONSE
