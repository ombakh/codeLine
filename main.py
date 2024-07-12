import os
from openai import OpenAI
from dotenv import load_dotenv
import tkinter as tk

load_dotenv()
client = OpenAI()

def get_query():
    query = text_box.get("1.0", tk.END).strip()  # Retrieve content from the text box
    if query:
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an extremely knowledgeable and highly educated assistant. You are extremely skilled at writing programs and helping debug."},
                    {"role": "user", "content": query}
                ]
            )
            # Access the content of the message directly
            response = completion.choices[0].message.content
            response_label.config(text=response)  # Update response label
        except Exception as e:
            response_label.config(text=f"Error: {str(e)}\nType: {type(e)}")  # Display error message
    else:
        response_label.config(text="Please enter a query.")

# Rest of the code remains the same
root = tk.Tk()
root.geometry("800x800")
root.title("code.ine")

title_label = tk.Label(root, text="code.ine")
title_label.pack(padx=10, pady=10)

text_box = tk.Text(root, width=50, height=10)
text_box.pack(padx=10, pady=10)

send_button = tk.Button(root, text="->", command=get_query)
send_button.pack(padx=10, pady=10)

response_label = tk.Label(root, text="", wraplength=780)  # Added wraplength for better text wrapping
response_label.pack(padx=10, pady=10)

root.mainloop()