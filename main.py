import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are an extremely knowledgeable and highly educated assistant. You are extremely skilled at writing programs and helping debug."},
    {"role": "user", "content": "Write me insertion sort in python."}
  ]
)

print(completion.choices[0].message)