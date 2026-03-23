import os
import argparse
from dotenv import load_dotenv

from google import genai
from google.genai import types


def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("unable to located api key")
    client = genai.Client(api_key=api_key)




    parser = argparse.ArgumentParser(description="command line tool")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
    model = "gemini-2.5-flash", contents=messages
)
    if response.usage_metadata is None:
        raise RuntimeError("no token information available")
    if args.verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)


if __name__ == "__main__":
    main()
