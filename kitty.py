import ollama
import time
from tkinter import *
import pyautogui

class Agent:
    "The Agent class is required to chat with ollama"
    def __init__(self, model='mistral', system=''):
        self.messages = [self.create_message(system, "system")] #
        self.model=model

    def create_message(self, message, role):
        return {
            'role': role,
            'content': message
        }

    # Starting the main conversation loop
    def chat(self):
        streamLabel.configure(text="Asking to "+self.model+"...")
        streamLabel.update()
        response = ollama.chat(model=self.model, messages=self.messages, stream=True)
        assistant_message=""
        streamLabel.configure(text="Printing " + self.model + " reponse...")
        streamLabel.update()
        for chunk in response:
            token=chunk["message"]["content"]
            assistant_message+=token
            streamLabel.configure(text=assistant_message)
            streamLabel.update()
            if len(assistant_message.split("\n")[-1])>=60:
                assistant_message+="\n"

        print()
        self.messages.append(self.create_message(assistant_message, 'assistant'))
        return assistant_message

    def ask(self, message):
        self.messages.append(
            self.create_message(message, 'user')
        )
        return self.chat()

def submit(send_screen):
    msg=entry.get()

    if send_screen:
        pyautogui.screenshot("screen.jpg")
        llava.messages.append({"role" : "user", "content" : msg, "images" : ["screen.jpg"]})
        llava.chat()
    else:
        kitty.ask(msg)


kitty=Agent(model="mistral")
llava=Agent(model="llava")
tk=Tk()
tk.title("Kitty")
tk.wm_attributes("-topmost", 1)
entry=Entry(tk)
entry.bind("<KeyPress-Return>", lambda e: submit(True))
entry.grid(column=0, row=0)
Button(tk, text="Send with screenshot", command=lambda:submit(True)).grid(column=1, row=0)
Button(tk, text="Send without screenshot", command=lambda:submit(False)).grid(column=1, row=1)
streamLabel=Label(tk, text="Ask a question to start...", width=50)
streamLabel.grid(row=2)
tk.mainloop()