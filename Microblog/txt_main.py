import os, time, getpass

users = {}
posts = {'all_users': []}
current_users = []

menu_1_text = '''
    -----------------------
    | 1] login to program |
    -----------------------
    | 2] create new user  |
    -----------------------
    | 3] exit program     |
    -----------------------
'''
menu_2_text = '''
    -----------------------
    | 1] create new post  |
    -----------------------
    | 2] view the wall    |
    -----------------------
    | 3] send a message   |
    -----------------------
    | 4] view your inbox  |
    -----------------------
    | 5] follow a user    |
    -----------------------
    | 6] logout           |
    -----------------------
'''

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
        self.set_creds()

    def set_creds(self):
        os.system('clear')
        print('Create A New User: \n')
        self.name = input("Enter your name: ")
        chosen_user = input("Enter a username: ")
        while chosen_user in current_users:
            os.system('clear')
            print("This username already exists!")
            chosen_user = input("Enter a username: ")
        self.username = chosen_user
        self.password = hash(getpass.getpass("Enter a password: "))
        users[self.username] = self
        posts[self.username] = []
        get_current_users()
    
    def new_post(self):
        os.system('clear')
        print('New Post: \n')
        post = Message(self.name)
        posts['all_users'].append(post)
        posts[self.username].append(post.message)
    
    def view_posts(self):
        os.system('clear')
        print('View Wall: \n')
        for post in posts['all_users']:
            print("{0}: {1}".format(post.user,post.message))
            time.sleep(0.5)
    
    def send_message(self):
        os.system('clear')
        print('Send A Message: \n')
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
                    os.system('clear')
                    print(current_users)
                    n = input("Who do you want to send your message to? (enter a username): ")
                user = n
            message = Message(self.name)
            users[user].inbox.append(message)
            current_users.append(self.username)
    
    def view_inbox(self):
        os.system('clear')
        print('View Inbox: \n')
        #goes through every message
        for message in self.inbox:
            print("From {0}: {1}".format(message.user,message.message))
            time.sleep(0.5)
            self.inbox.remove(message)
    
    def follow_user(self):
        os.system('clear')
        print('Follow A User: \n')
        if len(current_users) == 1:
            print("There are no other users :(")
        else:
            current_users.remove(self.username)
            print(current_users)
            n = input("Who do you want to follow? (enter a username): ")
            #making sure the user picks an existing username that is not their own
            if n in current_users:
                user = n
            else:
                while n not in current_users:
                    os.system('clear')
                    print(current_users)
                    n = input("Who do you want to follow? (enter a username): ")
                user = n
            users[user].followers_count += 1
            users[user].followers.append(self.username)
            current_users.append(self.username)
            print(users[user].followers)

def program(user):
    os.system('clear')
    print("Welcome {0}!".format(user.username))
    logged_in_menu = Menu(2, user)
    while logged_in_menu.response != 6:
        response = logged_in_menu.response
        if response == 1: #post
            user.new_post()
        elif response == 2: #wall
            user.view_posts()
        elif response == 3: #message
            user.send_message()
        elif response == 4: #inbox
            user.view_inbox()
        elif response == 5: #follow
            user.follow_user()
        time.sleep(3)
        input('\npress [enter] to go back to menu')
        logged_in_menu = Menu(2, user)
    return None

class Menu:
    def __init__(self, mode, user=None):
        self.response = None
        self.user = user
        if mode == 1:
            self.init_menu()
        else:
            self.program_menu()

    def init_menu(self):
        os.system('clear')
        print('Menu Choices: ')
        print(menu_1_text)
        n = int(input("What do you want to do? (1/2/3): "))
        while n != 1 and n != 2 and n != 3:
            os.system('clear')
            print('Menu Choices: ')
            print(menu_1_text)
            n = int(input("What do you want to do? (1/2/3): "))
        self.response = n
    def program_menu(self):
        os.system('clear')
        print("{0}'s Dashboard: ".format(self.user.name))
        print(menu_2_text)
        n = int(input("What do you want to do? (1/.../6): "))
        while n > 6 or n < 1:
            os.system('clear')
            print("{0}'s Dashboard: ".format(self.user.name))
            print(menu_2_text)
            n = int(input("What do you want to do? (1/.../6): "))
        self.response = n

def login():
    os.system('clear')
    print('Login: \n')
    get_current_users()
    chosen_user = input("Username: ")
    while chosen_user not in current_users:
        print("Username does not exist!")
        n = input("Do you want to create a user? (y/n): ")
        while n != 'y' and n != 'n':
            os.system('clear')
            print("Enter an acceptable answer.")
            n = input("Do you want to create a user? (y/n): ")
        if n == 'y':
            User()
        m = input("Try logging in again? (y/n): ")
        while m != 'y' and m != 'n':
            os.system('clear')
            print("Enter an acceptable answer.")
            m = input("Try logging in again? (y/n): ")
        if m == 'y':
            chosen_user = input("Username: ")
        else:
            return False
    chosen_pass = hash(getpass.getpass("Password: "))
    while chosen_pass != users[chosen_user].password:
        print("Invalid password!")
        m = input("Try logging in again? (y/n): ")
        while m != 'y' and m != 'n':
            os.system('clear')
            print("Enter an acceptable answer.")
            m = input("Try logging in again? (y/n): ")
        if m == 'y':
            chosen_pass = hash(getpass.getpass("Password: "))
        else:
            return False
    return [chosen_user, True]

def main():
    first_menu_choice = Menu(1)
    while first_menu_choice.response != 3:
        #LOG INTO PROGRAM
        if first_menu_choice.response == 1:
            get_current_users()
            if current_users == None or current_users == []:
                os.system('clear')
                print('There are no current users.')
                time.sleep(2.5)
                os.system('clear')
                for x in range(10):
                    print('Redirecting{0}'.format('.' * (x+1)))
                    time.sleep(0.5)
                    os.system('clear')
                User()
            user_login = login()
            if user_login[1]:
                program(users[user_login[0]])
            else:
                break

        #MAKE A NEW USER
        if first_menu_choice.response == 2:
            #must run this every time you make new user!!!
            User()

        first_menu_choice = Menu(1)
    return None

os.system('clear')
start_up_input = input("")
while start_up_input != 'exit':
    os.system('clear')
    for x in range(10):
        print("Starting{0}".format('.' * (x+1)))
        time.sleep(0.5)
        os.system('clear')
    main()
    os.system('clear')
    start_up_input = input("")
os.system('clear')