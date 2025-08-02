import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        dir_path = os.path.abspath(full_path)
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
            raise Exception(f"Error: Cannot list {directory} as it is outside the permitted working directory")
        elif not os.path.isdir(dir_path):
            raise Exception(f"Error: {directory} is not a directory")
        else:
            items = os.listdir(dir_path)
            def format_item(item):
                item_path = os.path.join(dir_path, item)
                return f" - {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
            items_string = "\n".join(map(format_item, items))
            return items_string
    except Exception as e:
         return e

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)