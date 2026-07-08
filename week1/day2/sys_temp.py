# three roles 
# system
# user 
# assistant

import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(Path(__file__).resolve().parent.parent.parent /".env")

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API KEY not FOUND")

client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"
role = "user"
prompt = "write a poem about a river and a sea"

#SYSTEM
message_system = {
    "role": "system",
    "content": "You are a wise and Old poet who writes poems about nature and the environment."
}

#message role and content

message = {
    "role": role,
    "content": prompt
}
message = [message_system, message]

response = client.chat.completions.create(model= model, messages = message, temperature = 0)
print("=================================================")  
answer = response.choices[0].message.content
print(answer)

