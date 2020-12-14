import os, time, getpass, random

#local databases, will configure different ones in the future
users = {}
posts = {'all_users': []}
current_users = []

#CUSTOM ASCII ART MENUS
menu_1_text = '''
    -----------------------
    | 1] login to program |
    |---------------------|
    | 2] create new user  |
    |---------------------|
    | 3] exit program     |
    -----------------------
'''
menu_2_text = '''
    -----------------------
    | 1] view profile     |
    |---------------------|
    | 2] create new post  |
    |---------------------|
    | 3] view the wall    |
    |---------------------|
    | 4] send a message   |
    |---------------------|
    | 5] view your inbox  |
    |---------------------|
    | 6] follow a user    |
    |---------------------|
    | 7] logout           |
    -----------------------
'''

def get_current_users():
    global current_users
    current_users = [username for username in users.keys()]

class Message: #message class
    def __init__(self, user):
        self.user = user
        self.message = input("Enter a message: ")

class User: #BIIIIIGGGGG user class
    def __init__(self):
        #just some class stuff
        self.name = None
        self.username = None
        self.password = None
        self.inbox = []
        self.followers = []
        self.logged_in = False
        self.set_creds()

    def set_creds(self):
        os.system('clear')
        print('Create A New User: \n')
        self.name = input("Enter your name: ")
        chosen_user = input("Enter a username: ")
        while chosen_user in current_users: #makes sure usernames aren't duplicated
            os.system('clear')
            print("This username already exists!")
            chosen_user = input("Enter a username: ")
        self.username = chosen_user
        self.password = hash(getpass.getpass("Enter a password: "))
        users[self.username] = self
        posts[self.username] = []
        get_current_users()

    def view_profile(self):
        os.system('clear')
        print('Your Profile: \n')
        labels = ['Name', 'Username', 'Followers']
        selfvars = [self.name, self.username, len(self.followers)]
        max_char = 0
        for index,label in enumerate(labels):
            test_string = '| {0}:  |'.format(label)
            for char in str(selfvars[index]):
                test_string += char
            if max_char < len(test_string):
                max_char = len(test_string)
        print('{0}'.format('-' * max_char))
        for index, label in enumerate(labels):
            count = 1
            string = '| {0}: {1}{2} {3}'.format(label, selfvars[index], '', '|')
            while len(string) < max_char:
                string = '| {0}: {1}{2} {3}'.format(label, selfvars[index], ' '*(count), '|')
                count += 1
            print(string)
            if index != 2:
                print('|{0}|'.format('-' * (max_char-2)))
        print('{0}'.format('-' * max_char))

    def new_post(self): #new post
        os.system('clear')
        print('New Post: \n')
        post = Message(self.name)
        posts['all_users'].append(post)
        posts[self.username].append(post.message)

    def view_posts(self): #view all posts by all users
        os.system('clear')
        print('View Wall: \n')
        for post in posts['all_users']:
            print("{0}: {1}".format(post.user,post.message))
            time.sleep(0.5)

    def send_message(self):
        os.system('clear')
        print('Send A Message: \n')
        if len(current_users) == 1: #need a different user for this function
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
        if len(self.inbox) == 0:
            print('There is nothing here :/')
        else:
            for message in self.inbox:
                print("From {0}: {1}".format(message.user,message.message))
                time.sleep(1.5)
            self.inbox = []

    def follow_user(self):
        os.system('clear')
        print('Follow A User: \n')
        bad_users = []
        if self.username in current_users:
            current_users.remove(self.username)
            bad_users.append(self.username)
        for user in users: #removes any users that the current user already follows
            if self.username in users[user].followers and user in current_users:
                bad_users.append(user)
                current_users.remove(user)
        if len(current_users) == 0: #need another user for this function
            print("There are no other users :(")
        else:
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
            users[user].followers.append(self.username)
            n = input("Do you want to follow another user? (y/n): ")
            if n == 'y': #try again -- don't really care if the human doesn't input correct response... they will answer 'y' if they want to try again
                self.follow_user()
        for user in bad_users: #adds every removed user back into current user list
            current_users.append(user)

def program(user): #USER DASHBOARD
    os.system('clear')
    logged_in_menu = Menu(2, user)
    while logged_in_menu.response != 7: #keeps the program running while user is logged in
        response = logged_in_menu.response
        get_current_users()
        if response == 1: #profile
            user.view_profile()
        elif response == 2: #post
            user.new_post()
        elif response == 3: #wall
            user.view_posts()
        elif response == 4: #message
            user.send_message()
        elif response == 5: #inbox
            user.view_inbox()
        elif response == 6: #follow
            user.follow_user()
        input('\npress [enter] to go back to menu') #stops content from being erased too quickly
        logged_in_menu = Menu(2, user)
    return None

class Menu: #DIFFERENT MENUS
    def __init__(self, mode, user=None):
        self.response = None
        self.user = user
        if mode == 1:
            self.init_menu()
        else:
            self.program_menu()

    def init_menu(self): #initial home screen menu
        os.system('clear')
        print('Menu Choices: ')
        print(menu_1_text)
        n = int(input("What do you want to do? (1/2/3): "))
        while n != 1 and n != 2 and n != 3: #ensures available options are chosen
            os.system('clear')
            print('Menu Choices: ')
            print(menu_1_text)
            n = int(input("What do you want to do? (1/2/3): "))
        self.response = n
    def program_menu(self): #user dashboard menu
        os.system('clear')
        print("{0}'s Dashboard: ".format(self.user.username))
        print(menu_2_text)
        n = int(input("What do you want to do? (1/.../7): "))
        while n > 7 or n < 1: #ensures available options are chosen
            os.system('clear')
            print("{0}'s Dashboard: ".format(self.user.username))
            print(menu_2_text)
            n = int(input("What do you want to do? (1/.../7): "))
        self.response = n

def login(): #LOGIN FUNCTION
    os.system('clear')
    print('Login: \n')
    get_current_users()
    chosen_user = input("Username: ")
    while chosen_user not in current_users:
        print("Username does not exist!")
        #gives user option to make a user
        n = input("Do you want to create a user? (y/n): ")
        if n == 'y': #don't care if human doesn't input correct response... they will answer 'y' if they want to create user
            User()
        m = input("Try logging in again? (y/n): ")
        #gives user option to try again
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
        #gives user option to try again
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
    print("Welcome to Pinsta!")
    time.sleep(2.5)
    first_menu_choice = Menu(1)
    while first_menu_choice.response != 3:
        #LOG INTO PROGRAM
        if first_menu_choice.response == 1:
            get_current_users()
            #need a user to be able to log in
            if current_users == None or current_users == []:
                os.system('clear')
                #forces user to create a new user for this function
                print('There are no current users.')
                time.sleep(2.5)
                os.system('clear')
                for x in range(10):
                    print('Redirecting{0}'.format('.' * (x+1)))
                    time.sleep(0.5)
                    os.system('clear')
                User()
                #LOGGING IN
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

#a lot of this is unnecessary... just for my preferences :)
os.system('clear')
start_up_input = input("press [enter] to start or type 'exit' to end: ")
while start_up_input != 'exit':
    os.system('clear')
    for x in range(random.randint(10, 50)): #made it a random length just for funsies
        print("Starting{0}".format('.' * (x+1)))
        time.sleep(0.1)
        os.system('clear')
    main()
    os.system('clear')
    start_up_input = input("press [enter] to start or type 'exit' to end: ")
os.system('clear')