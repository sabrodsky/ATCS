import os, time, getpass, random, shelve, hashlib

#SET UP
admin_passkey = 'admin'
usernames = []

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
    | 1] view a profile   |
    |---------------------|
    | 2] edit info        |
    |---------------------|
    | 3] create new post  |
    |---------------------|
    | 4] view the wall    |
    |---------------------|
    | 5] send a message   |
    |---------------------|
    | 6] view your inbox  |
    |---------------------|
    | 7] follow a user    |
    |---------------------|
    | 8] view followers   |
    |---------------------|
    | 9] delete account   |
    |---------------------|
    | 10] logout          |
    -----------------------
'''

def db_init():
    title('Initialize database: \n')
    with shelve.open('microblog') as db:
        db['users'] = {}
        db['posts'] = {'all_users': []}
        db['inboxes'] = {}
        db['followers'] = {}

    n = int(input("How many users?: "))
    with shelve.open('microblog') as db:
        users = db['users']
        for _ in range(n):
            new_user = User()
            users[new_user.username] = new_user
            input("\nSuccess! press [enter] to continue ")
        db['users'] = users

def get_current_users():
    global usernames
    usernames = []
    with shelve.open('microblog') as db:
        for user in db['users']:
            usernames.append(user)

def d(subset, key):
    #ex: d(users,username) deletes the username and username's value in the user database
    with shelve.open('microblog') as db:
        sect = db[subset]
        del sect[key]
        db[subset] = sect

def title(title):
    os.system('clear')
    print(title)

class Message: #message class
    def __init__(self, username):
        self.username = username
        self.message = input("Enter a message: ")

    def new_post(self): #user is the current user
        with shelve.open('microblog') as db:
            posts = db['posts']

            title('New Post: \n')
            posts['all_users'].append(self)
            posts[self.username].append(self)

            db['posts'] = posts
        print("Post has successfully been made!")

    def send_message(self): #user is the recipient
        with shelve.open('microblog') as db:
            inbox = db['inboxes']

            get_current_users()
            title('Send Message: \n')
            usernames.remove(self.username)
            if len(usernames) == 0: #need another user for this function
                print("There are no other users :(")
            else:
                print('Available Users: ', usernames)
                n = input("Who do you want to send your message to? [enter username]: ")
                #making sure the user picks an existing username that is not their own
                if n in usernames:
                    user = n
                else:
                    while n not in usernames:
                        os.system('clear')
                        print('Available Users: ', usernames)
                        n = input("Who do you want to send your message to? [enter username]: ")
                    user = n
            inbox[user].append(self)

            db['inboxes'] = inbox

def update_posts(username):
    with shelve.open('microblog') as db:
        posts = db['posts']

        for post in posts['all_users']:
            if post.username == username:
                post.username = '[deleted]'

        db['posts'] = posts

def view_posts(): #view all posts by all users
    get_current_users()
    with shelve.open('microblog') as db:
        posts = db['posts']

        title('View Wall: \n')
        if len(posts['all_users']) != 0:
            for post in posts['all_users']:
                print("{0}: {1}".format(post.username, post.message))
                time.sleep(1)
        else:
            print("There are no posts yet. :(")

        db['posts'] = posts

class User: #BIIIIIGGGGG user class
    def __init__(self, name=None, username=None, password=None, mode=None):
        #just some class stuff
        self.name = name
        self.username = username
        self.password = password
        self.mode = mode

        self.set_creds()

    def set_creds(self):
        with shelve.open('microblog') as db:
            users = db['users']
            posts = db['posts']
            inbox = db['inboxes']
            follow = db['followers']

            get_current_users()
            if self.mode == None:
                title('Create A New User: \n')
            elif self.mode == 'n':
                title('Change Name: \n')
            elif self.mode == 'u':
                title('Change Username: \n')
            else:
                title('Change Password: \n')

            if self.name == None:
                self.name = input("Enter your name: ")
            if self.username == None:
                chosen_user = input("Enter a username: ")
                while chosen_user in usernames: #makes sure usernames aren't duplicated
                    os.system('clear')
                    print("This username already exists!")
                    chosen_user = input("Enter a username: ")
                self.username = chosen_user
                posts[self.username] = []
                inbox[self.username] = []
                follow[self.username] = []
            if self.password == None:
                pass1 = getpass.getpass("Enter password: ")
                pass2 = getpass.getpass("Re-enter password: ")
                while hashlib.sha256(pass1.encode('utf-8')).digest() != hashlib.sha256(pass2.encode('utf-8')).digest():
                    print("Passwords must match!")
                    pass1 = getpass.getpass("Enter password: ")
                    pass2 = getpass.getpass("Re-enter password: ")
                self.password = hashlib.sha256(pass1.encode('utf-8')).digest()

            db['users'] = users
            db['posts'] = posts
            db['inboxes'] = inbox
            db['followers'] = follow

    def edit_creds(self):
        with shelve.open('microblog') as db:
            users = db['users']
            posts = db['posts']
            inbox = db['inboxes']
            follow = db['followers']

            title('Edit Your Information: \n')
            user_choice = input("Do you want to change your name, username, or password? (n/u/p): ")
            while user_choice != 'n' and user_choice != 'u' and user_choice != 'p':
                os.system('clear')
                print("Enter an acceptable answer.")
                user_choice = input("Do you want to change your name, username, or password? (n/u/p): ")
            if user_choice == 'n':
                new_user = User(username=self.username, password=self.password, mode='n')
                users[new_user.username] = new_user
            elif user_choice == 'u':
                new_user = User(name=self.name, password=self.password, mode='u')
                users[new_user.username] = new_user

                self.user_update(self.username, new_user.username) #updates user, post, inbox, and follow dictionaries

                return_name = new_user.username
            elif user_choice == 'p':
                new_user = User(name=self.name, username=self.username, mode='p')
                users[new_user.username] = new_user

            db['users'] = users
            db['posts'] = posts
            db['inboxes'] = inbox
            db['followers'] = follow

        return new_user.username

    def view_profile(self):
        global usernames
        with shelve.open('microblog') as db:
            users = db['users']
            follow = db['followers']

            title('View A Profile: \n')
            get_current_users()
            print("Available Users: ", usernames)
            chosen_user = input("Whose profile do you want to view?: ")
            while chosen_user not in usernames:
                os.system('clear')
                print("Choose an existing user.")
                print("Available Users: ", usernames)
                chosen_user = input("Whose profile do you want to view?: ")
            title("{0}'s Profile: \n".format(users[chosen_user].username))
            labels = ['Name', 'Username', 'Followers']
            selfvars = [users[chosen_user].name, users[chosen_user].username, len(follow[chosen_user])]
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

            db['followers'] = follow
            db['users'] = users

    def view_inbox(self):
        with shelve.open('microblog') as db:
            inbox = db['inboxes']

            title('View Inbox: \n')
            #goes through every message
            if len(inbox[self.username]) == 0:
                print('There is nothing here :/')
            else:
                for message in inbox[self.username]:
                    print("From {0}: {1}".format(message.username,message.message))
                    time.sleep(1.5)
                inbox[self.username] = []

            db['inboxes'] = inbox

    def follow_user(self):
        global usernames
        get_current_users()
        running = True
        while running:
            del_users = []
            with shelve.open('microblog') as db:
                follow = db['followers']
                title('Follow A User: \n')
                if self.username in usernames: #cannot follow yourself
                    usernames.remove(self.username)
                for user in usernames: #removes any users that the current user already follows
                    if self.username in follow[user]:
                        del_users.append(user)
                for user in del_users: #needed two lists because removing an item while in a for loop changes the indices of the items, causing some items to be skipped
                    usernames.remove(user)
                if len(usernames) == 0: #need another user for this function
                    print("There are no other users :(")
                    running = False
                else:
                    print('Available Users: ', usernames)
                    n = input("Who do you want to follow? [enter username]: ")
                    #making sure the user picks an existing username that is not their own
                    if n in usernames:
                        user = n
                    elif n not in usernames and n == '':
                        break
                    else:
                        while n not in usernames:
                            os.system('clear')
                            print('Available Users: ', usernames)
                            n = input("Who do you want to follow? [enter username]: ")
                        user = n
                    follow[user].append(self.username)
                    n = input("Do you want to follow another user? (y/n): ")
                    if n != 'y': #try again -- don't really care if the human doesn't input correct response... they will answer 'y' if they want to try again
                        running = False
                    else:
                        usernames.remove(user)

                db['followers'] = follow

    def view_follow(self):
        global usernames
        with shelve.open('microblog') as db:
            users = db['users']
            follow = db['followers']

            title('View Followers: \n')
            get_current_users()
            print("Available Users: ", usernames)
            chosen_user = input("Whose follower list do you want to view?: ")
            while chosen_user not in usernames:
                os.system('clear')
                print("Choose an existing user.")
                print("Available Users: ", usernames)
                chosen_user = input("Whose follower list do you want to view?: ")
            title("{0}'s Follow List: \n".format(users[chosen_user].username))
            followers = follow[chosen_user]
            max_char = 0
            for index,follower in enumerate(followers):
                test_string = '| {0}:  |'.format(follower)
                for char in str(followers[index]):
                    test_string += char
                if max_char < len(test_string):
                    max_char = len(test_string)
            print('{0}'.format('-' * max_char))
            for index, follower in enumerate(followers):
                count = 1
                string = '| {0}: {1}{2} {3}'.format(follower, followers[index], '', '|')
                while len(string) < max_char:
                    string = '| {0}: {1}{2} {3}'.format(follower, followers[index], ' '*(count), '|')
                    count += 1
                print(string)
                if index != 2:
                    print('|{0}|'.format('-' * (max_char-2)))
            print('{0}'.format('-' * max_char))

            db['followers'] = follow
            db['users'] = users

    def delete_user(self):
        with shelve.open('microblog') as db:
            inbox = db['inboxes']

            title("Delete User: \n")
            for label in ['users', 'followers', 'inboxes']:
                d(label, self.username)
            
            update_posts(self.username)

            for user in inbox:
                for message in inbox[user]:
                    if message.username == self.username:
                        message.username = '[deleted]'

            db['inboxes'] = inbox
            get_current_users()

    def user_update(self, user1, user2):
        get_current_users()
        with shelve.open('microblog') as db:
            posts = db['posts']
            inbox = db['inboxes']
            follow = db['followers']

            for user in usernames: #updates username in other inboxes
                for message in inbox[user1]:
                    if message.username == user1:
                        message.username = user2
            for message in inbox[user1]: #moves messages into other inbox
                inbox[user2].append(message)

            for user in usernames: #updates username in other follow lists
                for follower in follow[user1]:
                    if follower == user1:
                        follower = user2
            for follower in follow[user1]: #moves follows into other user list
                follow[user2].append(follower)

            for post in posts[user1]: #moves posts into other posts list
                posts[user2].append(post)
            for post in posts['all_users']: #changes post usernames
                if post.username == user1:
                    post.username = user2

            db['posts'] = posts
            db['inboxes'] = inbox
            db['followers'] = follow

def program(username): #USER DASHBOARD
    os.system('clear')
    with shelve.open('microblog') as db:
        users = db['users']
        user = users[username]
    logged_in_menu = Menu(2, user)
    while logged_in_menu.response != 10: #keeps the program running while user is logged in
        response = logged_in_menu.response
        get_current_users()
        if response == 1: #profile
            user.view_profile()
        elif response == 2: #edit
            new_user = user.edit_creds()
            for label in ['users', 'posts', 'followers', 'inboxes']:
                d(label, user.username)
            with shelve.open('microblog') as db:
                users = db['users']
                user = users[new_user]
        elif response == 3: #post
            with shelve.open('microblog') as db:
                posts = db['posts']
                input(posts[user.username])
            post = Message(user.username)
            post.new_post()
        elif response == 4: #wall
            view_posts()
        elif response == 5: #send
            post = Message(user.username)
            post.send_message()
        elif response == 6: #inbox
            user.view_inbox()
        elif response == 7: #follow
            user.follow_user()
        elif response == 8: #view followers
            user.view_follow()
        elif response == 9: #user
            user.delete_user()
            break
        input('\npress [enter] to go back to menu ') #stops content from being erased too quickly
        logged_in_menu = Menu(2, user)
    os.system('clear')
    for x in range(random.randint(10,20)):
        print('Logging out{0}'.format('.'*(x+1)))
        time.sleep(0.25)
        os.system('clear')
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
        title('Menu Choices: ')
        print(menu_1_text)
        n = int(input("What do you want to do? (1/2/3): "))
        while n > 3 or n < 1: #ensures available options are chosen
            title('Menu Choices: ')
            print(menu_1_text)
            n = int(input("What do you want to do? (1/2/3): "))
        self.response = n

    def program_menu(self): #user dashboard menu
        title("{0}'s Dashboard: ".format(self.user.username))
        print(menu_2_text)
        n = int(input("What do you want to do? (1/.../10): "))
        while n > 10 or n < 1: #ensures available options are chosen
            title("{0}'s Dashboard: ".format(self.user.username))
            print(menu_2_text)
            n = int(input("What do you want to do? (1/.../10): "))
        self.response = n

def login(): #LOGIN FUNCTION
    get_current_users()
    with shelve.open('microblog') as db:
        users = db['users']
        
        title('Login: \n')
        chosen_user = input("Username: ")
        chosen_pass = getpass.getpass("Password: ")
        if chosen_user not in users:
            print("Username does not exist!")
            time.sleep(2.5)
            return [chosen_user, False]
        elif users[chosen_user].password == hashlib.sha256(chosen_pass.encode('utf-8')).digest() or hashlib.sha256(chosen_pass.encode('utf-8')).digest() == hashlib.sha256(admin_passkey.encode('utf-8')).digest():
            time.sleep(2.5)
            return [chosen_user, True]
        else:
            return [chosen_user, False]
        
        db['users'] = users

def main():
    first_menu_choice = Menu(1)
    while first_menu_choice.response != 3:
        get_current_users()
        #LOG INTO PROGRAM
        if first_menu_choice.response == 1:
            #need a user to be able to log in
            if usernames == []:
                os.system('clear')
                #forces user to create a new user for this function
                print('There are no current users.')
                time.sleep(2.5)
            else:
                login_result = login()
                if login_result[1]:
                    program(login_result[0]) #pass in username

        elif first_menu_choice.response == 2:
            with shelve.open('microblog') as db:
                users = db['users']
                new_user = User()
                users[new_user.username] = new_user
                db['users'] = users

        first_menu_choice = Menu(1)
    return None

#a lot of this is unnecessary... just for my preferences :)
os.system('clear')
start_up_input = input("press [enter] to start or type 'exit' to end: ")
while start_up_input != 'exit':
    os.system('clear')
    if start_up_input == 'init':
        for x in range(random.randint(10, 50)):
            print("Initializing database{0}".format('.' * (x+1)))
            time.sleep(0.1)
            os.system('clear')
        db_init()
    for x in range(random.randint(10, 50)): #made it a random length just for funsies
        print("Starting{0}".format('.' * (x+1)))
        time.sleep(0.1)
        os.system('clear')
    main()
    os.system('clear')
    start_up_input = input("press [enter] to start or type 'exit' to end: ")
os.system('clear')
# os.system('python3 txt_main.py')