import os
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_wd = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_path.startswith(abs_wd):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        if not os.path.exists(os.path.dirname(target_path)):
            os.makedirs(os.path.dirname(target_path))
        with open(target_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the provided string in the specified file path, never outside the provided working directory. If such file does not exist as provided create it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path relative to the also provided working directory with the proper file extension",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write as string in the provided file",
            ),
        },
    ),
)