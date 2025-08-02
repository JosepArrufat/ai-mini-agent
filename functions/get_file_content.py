import os
from config import CHAR_LIMIT
from google.genai import types


def get_file_content(working_directory, file_path):
    cwd = os.path.abspath(".")
    joined_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(joined_path)
    if not abs_file_path.startswith(cwd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read()
            if len(file_content_string) > CHAR_LIMIT:
                return file_content_string[:CHAR_LIMIT] + f"...File '{file_path}' truncated at {CHAR_LIMIT} characters]"
            else:
                return file_content_string
    except Exception as e:
        return f"Error reading files: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return a string with the contents of the file path provided relative to the also provided working directory, limiting the character to return",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path from the also provided working directory",
            ),
        },
    ),
)
    