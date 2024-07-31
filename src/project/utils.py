from openai import OpenAI

from src.project.FeedbackPDF import FeedbackPDF


def gpt_api_request(project_files, project_feedback, api_key=None,
                    api_key_file=None):
    if api_key is None:
        if api_key_file is None:
            return "No API key provided"
        else:
            with open(api_key_file, "r") as f:
                api_key = f.read()

    feedback = "".join(project_feedback)
    contents = "".join(
        [file.file_name + ': ' + file.contents for file in project_files])
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
        print('-GPT API Request Successfully Made')
        return completion.choices[0].message.content

    except Exception as e:
        return None


def create_feedback_pdf(code_files, task, commit_log, summary, name):
    feedback_pdf = FeedbackPDF(task=task, summary=summary)
    feedback_pdf.add_commit_summary(commit_log)
    for file in code_files:
        feedback_pdf.add_code_with_feedback(file)
    feedback_pdf.output(f'{name} Task Feedback.pdf')
    print()
    print(f'{name} Task Feedback.pdf created')
