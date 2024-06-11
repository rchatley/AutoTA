import openai
import requests


def get_llm_summary(project, api_key=None, api_key_file=None):
    if api_key is None:
        if api_key_file is None:
            return "No API key provided"
        else:
            with open(api_key_file, "r") as f:
                openai.api_key = api_key
    else:
        openai.api_key = api_key

    feedback = project.feedback
    files = project.files

    try:
        messages = [
            {"role": "system",
             "content": "You are a helpful assistant that reviews Java code."},
            {"role": "user",
             "content": f"Project feedback:\n{feedback}\n"}
        ]

        for file in files:
            messages.append({"role": "user",
                             "content": f"Here is the content of Java file {file.file_name}:\n{file.contents}"})

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )

        return response.choices[0].message['content']

    except openai.error.OpenAIError as e:
        return f"OpenAI API error: {str(e)}"
    except requests.exceptions.RequestException as e:
        return f"Request error: {str(e)}"
    except ValueError as e:
        return f"Value error: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
