from openai import OpenAI


def get_llm_summary(project, api_key=None, api_key_file=None):
    if api_key is None:
        if api_key_file is None:
            return "No API key provided"
        else:
            with open(api_key_file, "r") as f:
                api_key = f.read()

    feedback = "".join(project.feedback)
    contents = "".join(
        [file.file_name + ': ' + file.contents for file in project.files])
    try:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a programming teaching assistant. Your "
                            "goal is to help university computing students "
                            "with their exercises by providing a concise "
                            "summary of feedback on their work. Review the "
                            "provided code and feedback, and offer a one-"
                            "paragraph summary of the code based almost "
                            "completely on the feedback."},
                {"role": "user",
                 "content": f"Given this code:\n\n```\n{contents}\n```\n\n"
                            f"and this feedback:\n\n{feedback}\n\n"
                            "Provide a one-paragraph summary of the coding "
                            "and potential improvements."}
            ]
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"An error occurred: {e}"
