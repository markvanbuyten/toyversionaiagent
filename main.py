import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from functions.call_functions import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise Exception("Gemini API Key was not found")

    client = genai.Client(api_key=api_key)

    prompt_parser = argparse.ArgumentParser(description = "Tutorial Chatbot")
    prompt_parser.add_argument("user_prompt", type=str, help="User prompt")
    prompt_parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    arguments = prompt_parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=arguments.user_prompt)])]

    model = "gemini-2.5-flash"
    #contents = arguments.user_prompt

    response = client.models.generate_content(model = model, 
        contents = messages,
        config = types.GenerateContentConfig(tools=[available_functions], system_instruction = system_prompt, temperature=0))

    if not response:
        raise RuntimeError("we had a failed API request")

    if arguments.verbose:
        print(f"User prompt: {messages}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    function_results = []

    if response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_call_result = call_function(part.function_call, verbose=arguments.verbose)
                if not function_call_result.parts:
                    raise Exception("Function call result has no parts.")

                first_part = function_call_result.parts[0]
                if first_part.function_response is None:
                    raise Exception("Function response is missing in the result parts.")
                
                if first_part.function_response.response is None:
                    raise Exception("The actual response field in FunctionResponse is None.")
                
                function_results.append(first_part)

                if arguments.verbose:
                    print(f"-> {first_part.function_response.response}")

            if part.text:
                print(f"{response.text}")


if __name__ == "__main__":
    main()
