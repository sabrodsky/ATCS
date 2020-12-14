import tkinter as tk
from tkinter import messagebox
import os, time

users = {}
posts = {'all_users': []}
current_users = []

def get_current_users():
    global current_users

    # users = open('user_list.txt', 'r')
    # for index, line in enumerate(users.readlines()):
    #     username = line[line.find('/')+2:line.rfind('/')-1]
    #     if username != "Username":
    #         current_users.append(username)
    # return current_users
    current_users = [username for username in users.keys()]

class User_Form:
    def __init__(self):
        self.name = None
        self.username = None
        self.password = None

        self.form()
    def form(self):
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
        #password
        self.pass_label = tk.Label(master=self.frm_form, text="Password:")
        self.pass_entry = tk.Entry(master=self.frm_form, width=15)
        self.pass_label.grid(row=2, column=0, sticky="e")
        self.pass_entry.grid(row=2, column=1)
        #submit button
        self.frm_buttons = tk.Frame()
        self.frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)
        self.btn_submit = tk.Button(master=self.frm_buttons, text="Submit", command=self.tk_submit)
        self.btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)
        #start application
        self.window.mainloop()
    def refresh(self):
        self.window.destroy()
        self.form()
    def tk_submit(self, *args):
        #assign user variables (finally!)
        self.name = self.name_entry.get()
        self.password = hash(self.pass_entry.get())
        chosen_username = self.user_entry.get()
        if chosen_username in users.keys():
            messagebox.showerror("Error", "Username is not available")
            self.refresh() #resets the window
        self.username = self.user_entry.get()
        #close application
        self.window.destroy()

class Login_Form:
    def __init__(self):
        self.response = False
        self.username = None

        self.window = tk.Tk()
        self.login()
    def login(self):
        # TKINTER HELL
        self.window.title("Login Window")
        self.frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
        self.frm_form.pack()
        #username
        self.user_label = tk.Label(master=self.frm_form, text="Username:")
        self.user_entry = tk.Entry(master=self.frm_form, width=15)
        self.user_label.grid(row=1, column=0, sticky="e")
        self.user_entry.grid(row=1, column=1)
        #password
        self.pass_label = tk.Label(master=self.frm_form, text="Password:")
        self.pass_entry = tk.Entry(master=self.frm_form, width=15)
        self.pass_label.grid(row=2, column=0, sticky="e")
        self.pass_entry.grid(row=2, column=1)
        #login button
        self.frm_buttons = tk.Frame()
        self.frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)
        self.btn_login = tk.Button(master=self.frm_buttons, text="Login", command=self.check_pass)
        self.btn_login.pack(side=tk.RIGHT, padx=10, ipadx=10)
        self.btn_cancel = tk.Button(master=self.frm_buttons, text="Cancel", command=self.cancel)
        self.btn_cancel.pack(side=tk.RIGHT, padx=10, ipadx=10)

        self.window.mainloop()
    def refresh(self):
        self.window.destroy()
        self.login()
    def cancel(self):
        self.response = False
        self.window.destroy()
    def check_pass(self, *args):
        chosen_user = self.user_entry.get()
        chosen_pass = hash(self.pass_entry.get())
        if chosen_user in current_users:
            if chosen_pass == users[chosen_user].password:
                self.response = True
            else:
                while chosen_pass != users[chosen_user].password:
                    messagebox.showerror("Error Message", 'Password is invalid.')
                    self.refresh()
        else:
            while chosen_user not in current_users:
                messagebox.showerror("Error Message", 'Username is invalid.')
                self.refresh()
        self.username = chosen_user
        self.window.destroy()

class Prompt:
    def __init__(self):
        self.response = None

        self.window = tk.Tk()
        self.prompt()
    def prompt(self):
        self.window.title("Prompt")

        text1 = tk.Text(self.window)
        text1.grid(row=0,column=0)
        text1.insert(tk.END, "Do you want to follow a user?")

        #the prompt
        btn_yes = tk.Button(self.window, text="Yes", command=self.yes)
        btn_yes.grid(row=1, column=0, sticky="nsew")
        btn_no = tk.Button(self.window, text="No", command=self.no)
        btn_no.grid(row=1, column=1, sticky="nsew")

        self.window.mainloop()
    def yes(self):
        self.response = True
        self.window.destroy()
    def no(self):
        self.response = False
        self.window.destroy()

class Message:
    def __init__(self, user):
        self.user = user
        self.message = input("Enter a message: ")

class User(User_Form):
    def __init__(self):
        #just some class stuff
        super().__init__()
        self.inbox = []
        self.followers_count = 0
        self.followers = []
        self.logged_in = False
    def new_post(self):
        post = Message(self.name)
        posts['all_users'].append(post)
        posts[self.username].append(post.message)
    def view_posts(self):
        for post in posts['all_users']:
            print("{0}: {1}".format(post.user,post.message))
    def send_message(self):
        if len(current_users) == 1:
            print("There are no other users :(")
        else:
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
            print("From {0}: {1}".format(message.user,message.message))
            self.inbox.remove(message)
    def follow_user(self):
        current_users.remove(self.username)
        print(current_users)
        n = input("Who do you want to follow? (enter a username): ")
        #making sure the user picks an existing username that is not their own
        if n in current_users:
            user = n
        else:
            while n not in current_users:
                print(current_users)
                n = input("Who do you want to follow? (enter a username): ")
            user = n
        users[user].followers_count += 1
        users[user].followers.append(self.username)
        current_users.append(self.username)
        print(users[user].followers)

def program(user):
    print("Welcome {0}!".format(user.username))
    logged_in_menu = Menu(2)
    response = logged_in_menu.response
    if response == 1: #post
        user.new_post()
    elif response == 2: #new user
        new_user = User()
        users[new_user.username] = new_user
        posts[new_user.username] = []
        get_current_users()
    elif response == 3: #message
        user.send_message()
    elif response == 4: #inbox
        user.view_inbox()
    elif response == 5: #follow
        user.follow_user()
    else:
        return None
    program(user)

class Menu:
    def __init__(self, mode):
        self.window = tk.Tk()
        self.response = None
        if mode == 1:
            self.menu_logged_out()
        if mode == 2:
            self.menu_logged_in()
    def menu_logged_out(self):
        self.window.title("Menu Window")

        frm_form = tk.Frame()
        frm_form.pack()

        login_button = tk.Button(master=frm_form, text='1', command=self.menu_login)
        login_button.grid(row=0, column=0)
        user_button = tk.Button(master=frm_form, text='2', command=self.menu_new_user)
        user_button.grid(row=1, column=0)
        exit_button = tk.Button(master=frm_form, text='3', command=self.menu_exit_program)
        exit_button.grid(row=2, column=0)

        login_label = tk.Label(master=frm_form, text='login to program')
        login_label.grid(row=0, column=1)
        user_label = tk.Label(master=frm_form, text='create new user')
        user_label.grid(row=1, column=1)
        exit_label = tk.Label(master=frm_form, text='exit program')
        exit_label.grid(row=2, column=1)

        self.window.mainloop()
    def menu_login(self):
        self.response = 1
        self.window.destroy()
    def menu_new_user(self):
        self.response = 2
        self.window.destroy()
    def menu_exit_program(self):
        if self.mode == 1:
            self.response = 3
        else:
            self.response = 5
        self.window.destroy()
    def menu_logged_in(self):
        self.window.title("Menu Window")

        frm_form = tk.Frame()
        frm_form.pack()

        post_button = tk.Button(master=frm_form, text='1', command=self.menu_post)
        post_button.grid(row=0, column=0)
        user_button = tk.Button(master=frm_form, text='2', command=self.menu_new_user)
        user_button.grid(row=1, column=0)
        message_button = tk.Button(master=frm_form, text='3', command=self.menu_message)
        message_button.grid(row=2, column=0)
        wall_button = tk.Button(master=frm_form, text='4', command=self.menu_wall)
        wall_button.grid(row=3, column=0)
        inbox_button = tk.Button(master=frm_form, text='5', command=self.menu_inbox)
        inbox_button.grid(row=3, column=0)
        follow_button = tk.Button(master=frm_form, text='6', command=self.menu_follow)
        follow_button.grid(row=4, column=0)
        exit_button = tk.Button(master=frm_form, text='7', command=self.menu_exit_program)
        exit_button.grid(row=5, column=0)

        post_label = tk.Label(master=frm_form, text='new post')
        post_label.grid(row=0, column=1)
        user_label = tk.Label(master=frm_form, text='new user')
        user_label.grid(row=1, column=1)
        message_label = tk.Label(master=frm_form, text='new message')
        message_label.grid(row=2, column=1)
        wall_label = tk.Label(master=frm_form, text='see posts')
        wall_label.grid(row=3, column=1)
        inbox_label = tk.Label(master=frm_form, text='see inbox')
        inbox_label.grid(row=4, column=1)
        follow_label = tk.Label(master=frm_form, text='follow user')
        follow_label.grid(row=5, column=1)
        exit_label = tk.Label(master=frm_form, text='logout')
        exit_label.grid(row=6, column=1)

        self.window.mainloop()
    def menu_post(self):
        self.response = 1
        self.window.destroy()
    def menu_message(self):
        self.response = 3
        self.window.destroy()
    def menu_wall(self):
        self.response = 4
        self.window.destroy()
    def menu_inbox(self):
        self.response = 5
        self.window.destroy()
    def menu_follow(self):
        self.response = 6
        self.window.destroy()

def main():
    first_menu_choice = Menu(1)

    #LOG INTO PROGRAM
    if first_menu_choice.response == 1:
        get_current_users()
        if current_users == None or current_users == []:
            new_user = User()
            users[new_user.username] = new_user
            posts[new_user.username] = []
        response_obj = Login_Form()
        if response_obj:
            user = users[response_obj.username]
            program(user)
        return None

    #MAKE A NEW USER
    if first_menu_choice.response == 2:
        #must run this every time you make new user!!!
        new_user = User()
        users[new_user.username] = new_user
        posts[new_user.username] = []
        get_current_users()
        main()

    #EXIT PROGRAM
    if first_menu_choice.response == 3:
        return None

start_up_input = input("")
while start_up_input != 'exit':
    os.system('clear')
    for x in range(5):
        print("Loading{0}".format('.' * x))
        time.sleep(1)
        os.system('clear')
    main()
    os.system('clear')
    start_up_input = input("")