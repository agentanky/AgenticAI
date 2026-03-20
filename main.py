import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("unable to located api key")

from google import genai

client = genai.Client(api_key=api_key)





def main():

    response = client.models.generate_content(
    model = "gemini-2.5-flash", contents="tell me about earth in one paragraph"
)
    if response.usage_metadata is None:
        raise RuntimeError("no token information available")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)


if __name__ == "__main__":
    main()
