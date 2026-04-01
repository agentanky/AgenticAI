import os
import argparse
from dotenv import load_dotenv
import sys

from google import genai
from google.genai import types
from prompts import system_prompt

from call_function import available_functions

from call_function import call_function


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
    for _ in range(20):
            
            response = client.models.generate_content(
            model = "gemini-2.5-flash", contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt, temperature = 0),
            
        )
            function_responses = []
            if response.candidates:
                for item in response.candidates:
                    messages.append(item.content)

            if response.usage_metadata is None:
                raise RuntimeError("no token information available")
            if args.verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            if response.function_calls is not None:
                for item in response.function_calls:
                    function_call_result = call_function(item, args.verbose)
                    if function_call_result.parts is None:
                        raise Exception("parts is none")
                    if function_call_result.parts[0].function_response is None:
                        raise Exception("parts response is empty")
                    if function_call_result.parts[0].function_response.response is None:
                        raise Exception("response empty")
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    function_responses.append(function_call_result.parts[0])
                messages.append(types.Content(role="user", parts=function_responses))
            else:
                print(response.text)
                break
    else:
        print(f"model has not produced final response")
        raise SystemExit(1)  
            


if __name__ == "__main__":
    main()
