import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from call_function import available_functions
from prompts import system_prompt
from functions.call_function import call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])])
    ]
    if len(sys.argv) > 1:
        for i in range(0, 20):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-001", 
                    contents=messages,
                    config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction={system_prompt}),
                )
                for candidate in response.candidates:
                    messages.append(types.Content(role="user", parts=candidate.content.parts))
                if not response.function_calls:
                    print(f"FINAL RESPONSE: {response.text}")
                    break
                if "--verbose" in sys.argv:
                    print(f"User prompt: {sys.argv[1]}")
                    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                print("----------------------")
                function_responses = []
                for function_call_part in response.function_calls:
                    verbose = "--verbose" in sys.argv
                    function_call_result = call_function(function_call_part, verbose)
                    if not function_call_result.parts[0].function_response.response:
                        raise Exception("Error: excpected some results from calling")
                    if verbose == True:
                        print(f"{function_call_result.parts[0].function_response.response}")
                    function_responses.append(function_call_result.parts[0])
                if not function_responses:
                    raise Exception("no function responses generated, exiting.")
                messages.append(types.Content(role="tool", parts=function_responses))   
            except:
                raise Exception("No response")
    else:
        print("No prompt provided")
        sys.exit(1)

if __name__ == "__main__":
    main()