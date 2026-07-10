import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key = my_api_key)

model="llama-3.3-70b-versatile"
role="user"

prompt1 = "Hi!"
prompt2 = "Explain time travel in Detail but under 100 words"
prompt3 = "Write a 1000 word essay on Machine learning"

prompts = [prompt1, prompt2, prompt3]
for prompt in prompts:
    message = {
        "role": role,
        "content": prompt
    }
    messages = [message]
    response = client.chat.completions.create(model = model, messages = messages, max_tokens = 5000)
    usage = response.usage
    print(f"Prompt::  {prompt} ---> Tokens used: {usage.prompt_tokens} completion tokens: {usage.completion_tokens} total tokens: {usage.total_tokens} Finish Reason: {response.choices[0].finish_reason}")




# prompt="write me a poem about the sun"
# # message me role and content
# message={
#     "role": role,
#     "content": prompt
# }

# messages=[message]

# response=client.chat.completions.create(model=model, messages=messages)
