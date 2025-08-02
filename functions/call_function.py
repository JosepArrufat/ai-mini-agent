from functions.write_file import write_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from google.genai import types


functions = {
    "write_file": write_file,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "get_files_info": get_files_info,
}

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else: 
        print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
    name = function_call_part.name
    function_result = functions[name]("./calculator", **function_call_part.args)
    if not functions[name]:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )    
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"result": function_result},
                )
            ],
        )