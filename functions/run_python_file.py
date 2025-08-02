import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    abs_wd = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_path.startswith(abs_wd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'
    if not target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        command = ["python", f"{file_path}"] + args
        result = subprocess.run( command,  cwd=abs_wd, capture_output=True, timeout=30, text=True)
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified file in file path through the subprocess, only within the provided working directory and called with the arguments only when pass it in command",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path from the also provided working directory",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The arguments to pass to the file_path file, only if provided by the user",
            ),
        },
    ),
)