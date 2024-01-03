import os


def read_file(file: str) -> str:
    file_exists = os.path.isfile(file)

    if file_exists is True:
        with open(file, "r") as file:
            token = file.read().rstrip()
            return token

    return ""


def write_to_file(filepath, content):
    content = str(content)
    with open(filepath, "w") as file:
        file.write(content)
