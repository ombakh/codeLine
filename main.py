from openai import OpenAI
from dotenv import load_dotenv
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import queue
import itertools

load_dotenv()
client = OpenAI()

purple_color = "#9F00FF"
red_color = "#FF0000"
black_color = "#000000"
white_color = "#FFFFFF"

class LoadingAnimation:
    def __init__(self, label, animation_type="text"):
        self.label = label
        self.is_animating = False
        self.animation_type = animation_type

        if animation_type == "text":
            self.frames = itertools.cycle(["-", "\\", "|", "/"])
        else:  # Unicode
            self.frames = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])

    def animate(self):
        if self.is_animating:
            frame = next(self.frames)
            self.label.config(text=f"code.ine\n{frame}")
            self.label.after(100, self.animate)

    def start(self):
        self.is_animating = True
        self.animate()

    def stop(self):
        self.is_animating = False

def get_query():
    query = text_box.get("1.0", tk.END).strip()
    if query:
        send_button.config(state=tk.DISABLED)
        loading_animation.start()
        Thread(target=process_query, args=(query,)).start()
        display_message(f"You: {query}")
        text_box.delete("1.0", tk.END)
    else:
        display_message("Please enter a query.", color=red_color)

def process_query(query):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are code.ine. You are an extremely knowledgeable and highly educated assistant. You are extremely skilled at writing programs and helping debug."},
                {"role": "user", "content": query}
            ]
        )
        response = completion.choices[0].message.content
        response_queue.put(response)
    except Exception as e:
        response_queue.put(f"Error: {str(e)}\nType: {type(e)}")
    root.after(0, update_response)

def update_response():
    try:
        response = response_queue.get_nowait()
        loading_animation.stop()
        display_message(f"code.ine: {response}")
    except queue.Empty:
        pass
    finally:
        send_button.config(state=tk.NORMAL)

def display_message(message, color=white_color):
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, message + "\n\n")
    chat_display.tag_add("color", chat_display.index("end-2l linestart"), chat_display.index("end-1c"))
    chat_display.tag_config("color", foreground=color)
    chat_display.see(tk.END)
    chat_display.config(state=tk.DISABLED)

root = tk.Tk()
root.geometry("800x600")
root.title("code.ine")

response_queue = queue.Queue()



title_label = tk.Label(root, text="{code.ine}", fg=purple_color, font=("SpaceMono-Regular", 16, "bold"))
title_label.pack(padx=10, pady=10)

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, bg=black_color, fg=white_color)
chat_display.pack(padx=10, pady=10)
chat_display.config(state=tk.DISABLED)

text_box = tk.Text(root, width=80, height=3)
text_box.pack(padx=10, pady=10)

send_button = tk.Button(root, text="?", command=get_query, fg=white_color, bg=black_color, font=("Arial", 16, "bold"))
send_button.pack(padx=10, pady=10)

loading_animation = LoadingAnimation(title_label, animation_type="unicode")

root.mainloop()