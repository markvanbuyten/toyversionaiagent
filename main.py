import os
import argparse
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise Exception("Gemini API Key was not found")

    client = genai.Client(api_key=api_key)

    prompt_parser = argparse.ArgumentParser(description = "Tutorial Chatbot")
    prompt_parser.add_argument("user_prompt", type=str, help="User prompt")
    arguments = prompt_parser.parse_args()

    model = "gemini-2.5-flash"
    contents = arguments.user_prompt

    response = client.models.generate_content(model = model, contents = contents)

    if not response:
        raise RuntimeError("we had a failed API request")

    print(f"User prompt: {contents}")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(f"{response.text}")


if __name__ == "__main__":
    main()
