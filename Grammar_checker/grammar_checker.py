import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent /".env")

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Groq Api key not found")

client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"
role = "user"

# BEHAVIOR
system_prompt = """
You are a professional English grammar and writing assistant.

Your task is to improve the user's writing while preserving its original meaning and tone.

Instructions:
- Correct grammar, spelling, punctuation, and capitalization.
- Improve sentence structure and readability.
- Preserve the original meaning and intent.
- Do not add or remove information unless necessary for grammatical correctness.
- Do not explain your changes.
- Do not include comments, notes, or formatting.
- If the text is already correct, return it unchanged.
- Return ONLY the improved text.
"""

#taking input
print("Enter your text (Press Enter twice to finish):")
lines = []
while True:
    line = input()
    if not line:
        break

    lines.append(line)

text = "\n".join(lines)
    
# what to do
user_prompt = f"""
Improve the grammar and readability of the following text while preserving its original meaning.

Text:
{text}
"""

system_message = {
    "role": "system",
    "content":system_prompt
}

message = {
    "role":role,
    "content": user_prompt
}
messages = [system_message, message]

response = client.chat.completions.create(model= model, messages=messages)

answer = response.choices[0].message.content

print(answer)