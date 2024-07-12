import os
from openai import OpenAI
from dotenv import load_dotenv
import tkinter as tk

load_dotenv()
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are an extremely knowledgeable and highly educated assistant. You are extremely skilled at writing programs and helping debug."},
    {"role": "user", "content": "What is the fastest way to write insertion sort in python"}
  ]
)

def get_query():
    query = text_box.get("1.0", tk.END)


#Creates window
root = tk.Tk()
root.geometry("800x800")
root.title("code.ine")

title_label = tk.Label(root, text="code.ine")
title_label.pack(padx=10, pady=10)

#Creates text entry box
text_box = tk.Text(root, width=50, height=10)
text_box.pack(padx=10, pady=10)

#Creates send button
send_button = tk.Button(root, text="->", command=get_query)
send_button.pack(padx=10, pady=10)

response = completion.choices[0].message
#Creates response label
response_label = tk.Label(root, text=response)
response_label.pack(padx=10, pady=10)


root.mainloop()


print(completion.choices[0].message)