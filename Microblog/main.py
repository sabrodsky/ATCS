import tkinter as tk
from tkinter import messagebox

users = {}
posts = {'all_users': []}
current_users = []

def get_current_users():
    current_users = [username for username in users]
    return current_users

class Message:
    def __init__(self, user):
        self.user = user
        self.message = input("Enter a message: ")

class User:
    def __init__(self):
        #just some class stuff
        self.name = None
        self.username = None
        self.inbox = []

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
        if chosen_username in users.keys():
            messagebox.showerror("Error", "Username is not available")
            self.window.destroy()
            self.tk_user_form()
        self.username = self.user_entry.get()
        #close application
        self.window.destroy()
    def new_post(self):
        post = Message(self.name)
        posts['all_users'].append(post)
        posts[self.username].append(post.message)
    def view_posts(self):
        for post in posts['all_users']:
            print("{0}: {1}".format(
                post.user,
                post.message
            ))
    def send_message(self):
        current_users.remove(self.username)
        print(current_users)
        n = input("Who do you want to send your message to? (enter a username): ")
        #making sure the user picks an existing username that is not their own
        if n in current_users:
            user = n
        else:
            while n not in current_users:
                print(current_users)
                n = input("Who do you want to send your message to? (enter a username): ")
            user = n
        message = Message(self.name)
        users[user].inbox.append(message)
        current_users.append(self.username)
    def view_inbox(self):
        #goes through every message
        for message in self.inbox:
            print("From {0}: {1}".format(
                message.user,
                message.message
            ))
            self.inbox.remove(message)

for _ in range(2):
    #must run this every time you make new user!!!
    new_user = User()
    users[new_user.username] = new_user
    posts[new_user.username] = []
    current_users = get_current_users()

for user in users: #returns the key rather than the value
    users[user].send_message()
    if len(users[user].inbox) >= 1:
        print("You have new messages!")
        users[user].view_inbox()
    else:
        print("You have no new messages!")