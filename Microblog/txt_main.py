# import tkinter as tk
# from tkinter import messagebox
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

class Message:
    def __init__(self, user):
        self.user = user
        self.message = input("Enter a message: ")

class User:
    def __init__(self):
        #just some class stuff
        self.name = None
        self.username = None
        self.password = None
        self.inbox = []
        self.followers_count = 0
        self.followers = []
        self.logged_in = False

    def set_creds(self):
        self.name = input("Enter your name: ")
        chosen_user = input("Enter a username: ")
        while chosen_user in current_users:
            print("This username already exists!")
            chosen_user = input("Enter a username: ")
        self.username = chosen_user
        self.password = hash(input("Enter a password: "))
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
        self.response = None

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
        print("Loading{0}".format('.' * x+1))
        time.sleep(1)
        os.system('clear')
    main()
    os.system('clear')
    start_up_input = input("")