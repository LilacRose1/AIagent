import sys
import os 
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if(api_key == None):
    raise RuntimeError("something up with your api key")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": args.user_prompt},]

    # Agent loop: keep letting the model call tools until it returns a plain
    # text response, or bail out after 20 rounds to avoid an infinite loop.
    for _ in range(20):

        response = client.chat.completions.create(
            model= "openrouter/free", 
            messages= messages, 
            tools=available_functions,)

        if(response.usage == None):

            raise RuntimeError("API request failed, something went wrong, check if everything is ok")

        elif(args.verbose == True):

            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message

        messages.append(message)
        # The model may request one or more tool calls in a single turn; run
        # each one and feed its result back before asking the model again.
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)
                if not result_message["content"]:
                    raise Exception("your function doesn't work as planned")

                if(args.verbose == True):
                    print(f"-> {result_message['content']}")
        else:
            print(message.content)
            return


    print("Agent failed to produce a final response after the maximum number of iterations.")
    sys.exit(1)



if __name__ == "__main__":
    main()
