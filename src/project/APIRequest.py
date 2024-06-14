from openai import OpenAI


def get_llm_summary(project, api_key=None, api_key_file=None):
    if api_key is None:
        if api_key_file is None:
            return "No API key provided"
        else:
            with open(api_key_file, "r") as f:
                api_key = api_key_file.read()

    feedback = "".join(project.feedback)
    contents = "".join(
        [file.file_name + ': ' + file.contents for file in project.files])

    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a programming teaching assistant, with the goal of helping university computing students with their exercises by providing a concise summary of feedback on their work."},
            {"role": "user",
             "content": "Given this code: " + contents + " and this feedback " + feedback + ". Give a one paragraph summary of the coding and potential improvements"}
        ]
    )

    return completion.choices[0].message.content
