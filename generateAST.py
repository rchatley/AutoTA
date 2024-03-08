import os

import javalang


def get_code(directory):
    java_file_contents = []

    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.java'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    source_code = file.read()
                java_file_contents.append(source_code)

    return java_file_contents


def get_asts(source_codes):
    return [javalang.parse.parse(source_code) for source_code in source_codes]


if __name__ == "__main__":
    java_source_directory = "SED3"

    file_contents = get_code(java_source_directory)
    asts = get_asts(file_contents)
