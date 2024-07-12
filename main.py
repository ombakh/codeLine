import os
from openai import OpenAI
from dotenv import load_dotenv
import tkinter as tk

load_dotenv()
client = OpenAI()

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are an extremely knowledgeable and highly educated assistant. You are extremely skilled at writing programs and helping debug."},
#     {"role": "user", "content": "Write me insertion sort in python."}
#   ]
# )

#def get_text():

root = tk.Tk()
root.geometry("800x800")
root.title("code.ine")
text_box = tk.Text(root, width=50, height=10)
text_box.pack(padx=10, pady=10)

send_button = tk.Button(root, text="->")
send_button.pack(padx=10, pady=10)

response_label = tk.Label(root, text="This is where the response will be displayed.")
response_label.pack(pady=10)


root.mainloop()



#print(completion.choices[0].message)