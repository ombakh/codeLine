import os
from openai import OpenAI
from dotenv import load_dotenv
import tkinter as tk
from threading import Thread
import queue
import itertools
import time

load_dotenv()
client = OpenAI()


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
            self.label.config(text=f"Processing {frame}")
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
    else:
        response_label.config(text="Please enter a query.")


def process_query(query):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are an extremely knowledgeable and highly educated assistant. You are extremely skilled at writing programs and helping debug."},
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
        response_label.config(text=response)
    except queue.Empty:
        pass
    finally:
        send_button.config(state=tk.NORMAL)


root = tk.Tk()
root.geometry("800x800")
root.title("code.ine")

response_queue = queue.Queue()

title_label = tk.Label(root, text="code.ine")
title_label.pack(padx=10, pady=10)

text_box = tk.Text(root, width=50, height=10)
text_box.pack(padx=10, pady=10)

send_button = tk.Button(root, text="->", command=get_query)
send_button.pack(padx=10, pady=10)

response_label = tk.Label(root, text="", wraplength=780)
response_label.pack(padx=10, pady=10)


loading_animation = LoadingAnimation(response_label, animation_type="unicode")

root.mainloop()