import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Groq api key not found")

client = Groq(api_key = my_api_key)

model="llama-3.3-70b-versatile"
role="user"

#structure it

from pydantic import BaseModel

class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schema = Ticket.model_json_schema()
response_format = {
    "type":"json_object"
}
system_prompt = f"""
Extract the personal information from the ticket strictly based on this schema and give me a json output.
"""
message_system = {
    "role":"system",
    "content": system_prompt
}


text = "Hello My name is prince. i was outside today and a girl harassed me . My adress is west bengal. my email prince@gmail.com.my contact number is 123456798"

prompt = f"This is a police complaint. Please extract the following information from the text: name,  issue, address, email, and contact number. here is the text: {text}. If any information is missing , please indicate that it is not available."

message = {
    "role": role,
    "content": prompt
}
messages = [message_system, message]
response = client.chat.completions.create(model = model, messages = messages, response_format=response_format)

answer = response.choices[0].message.content
print (answer)

import json 
raw_json = answer
data_file = json.loads(raw_json)
ticket = Ticket(**data_file)

print(ticket.name)
print(ticket.issue)
print(ticket.email)
