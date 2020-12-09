import tkinter as tk
from tkinter import messagebox

users = {}
posts = []
current_usernames = []

class Message:
    def __init__(self):
        self.message = input("Enter a message: ")

class User:
    def __init__(self):
        #just some class stuff
        self.name = None
        self.username = None
        self.tk_user_form()
    def tk_user_form(self):
        # TKINTER HELL
        self.window = tk.Tk()
        self.window.title("New User")
        self.frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
        self.frm_form.pack()
        #name
        self.name_label = tk.Label(master=self.frm_form, text="Name:")
        self.name_entry = tk.Entry(master=self.frm_form, width=15)
        self.name_label.grid(row=0, column=0, sticky="e")
        self.name_entry.grid(row=0, column=1)
        #username
        self.user_label = tk.Label(master=self.frm_form, text="Username:")
        self.user_entry = tk.Entry(master=self.frm_form, width=15)
        self.user_label.grid(row=1, column=0, sticky="e")
        self.user_entry.grid(row=1, column=1)
        self.frm_buttons = tk.Frame()
        self.frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)
        #submit button
        self.btn_submit = tk.Button(master=self.frm_buttons, text="Submit", command=self.tk_submit)
        self.btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)
        #start application
        self.window.mainloop()
    def tk_submit(self, *args):
        #assign user variables (finally!)
        self.name = self.name_entry.get()
        chosen_username = self.user_entry.get()
        while chosen_username in users.keys():
            messagebox.showerror("Error", "Username is not available")
            self.user_entry = tk.Entry(master=self.frm_form, width=15)
            self.user_entry.grid(row=1, column=1)
            chosen_username = self.user_entry.get()
        self.username = self.user_entry.get()
        #close application
        self.window.destroy()
    def new_post(self):
        post = Message()
        posts.append(post.message)
    def send_message(self):
        n = input("Who do you want to send your message to? (enter a username): ")
        #making sure the user picks an existing username
        if n in users.keys():
            user = n
        else:
            while n not in users.keys():
                n = input("Who do you want to send your message to? (enter a username): ")
            user = n
        message = Message()
        self.sent_messages.append(message)
        users[user].inbox.append(message)
    def view_inbox(self):
        #goes through every message
        for message in self.inbox:
            print(message.message)
            self.inbox.remove(message)
            #read messages are useless so... we delete them
            self.read_messages.append(message.message)

for _ in range(2):
    new_user = User()
    users[new_user.username] = User()
print(users)