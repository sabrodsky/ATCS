import os, time, getpass, random, shelve

admin_passkey = 'admin'
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
    | 1] view a profile   |
    |---------------------|
    | 2] edit info        |
    |---------------------|
    | 3] create new post  |
    |---------------------|
    | 4] delete post      |
    |---------------------|
    | 5] view the wall    |
    |---------------------|
    | 6] send a message   |
    |---------------------|
    | 7] view your inbox  |
    |---------------------|
    | 8] follow a user    |
    |---------------------|
    | 9] delete account   |
    -----------------------
    | 10] logout          |
    -----------------------
'''

def get_current_users():
    global current_users
    current_users = []

    #key in db should be the user's username
    with shelve.open('users') as users:
        for user in users:
            if users[user] != []:
                current_users.append(users[user].username)

class Message: #message class
    def __init__(self, user):
        self.user = user
        self.message = input("Enter a message: ")

class User: #BIIIIIGGGGG user class
    def __init__(self, name=None, username=None, password=None, mode='new'):
        #just some class stuff
        self.name = name
        self.username = username
        self.password = password
        self.mode = mode
        self.logged_in = False
        self.set_creds()

    def set_creds(self):
        with shelve.open('users') as users:
            os.system('clear')
            if self.mode == 'new':
                print('Create A New User: \n')
            else:
                print('Edit Information: \n')
            if self.name == None:
                self.name = input("Enter your name: ")
            if self.username == None:
                chosen_user = input("Enter a username: ")
                while chosen_user in current_users: #makes sure usernames aren't duplicated
                    os.system('clear')
                    print("This username already exists!")
                    chosen_user = input("Enter a username: ")
                self.username = chosen_user
                with shelve.open('followers') as f:
                    f[self.username] = []
                with shelve.open('inboxes') as inbox:
                    inbox[self.username] = []
                with shelve.open('posts') as p:
                    p[self.username] = []
            if self.password == None:
                self.password = hash(getpass.getpass("Enter a password: "))
            users[self.username] = self
            get_current_users()

    def edit_creds(self):
        with shelve.open('users') as users:
            os.system('clear')
            print('Edit Your Information: \n')
            user_choice = input("Do you want to change your name, username, or password? (n/u/p): ")
            while user_choice != 'n' and user_choice != 'u' and user_choice != 'p':
                os.system('clear')
                print("Enter an acceptable answer.")
                user_choice = input("Do you want to change your name, username, or password? (n/u/p): ")
            if user_choice == 'n':
                User(username=self.username, password=self.password, mode=None)
            elif user_choice == 'u':
                old_user = self.username
                users[old_user] = []
                with shelve.open('inboxes') as inbox:
                    inbox[old_user] = []
                with shelve.open('posts') as p:
                    p[old_user] = []
                new_user = User(name=self.name, password=self.password, mode=None)
                with shelve.open('followers') as f:
                    f[old_user] = []
                    for user in users:
                        if old_user in f[user]:
                            f[user].remove(old_user)
                            f[user].append(new_user.username)
            else:
                User(name=self.name, username=self.username, mode=None)

    def view_profile(self):
        with shelve.open('users') as users:
            os.system('clear')
            print('View A Profile: \n')
            get_current_users()
            print("Available Users: ", current_users)
            chosen_user = input("Whose profile do you want to view?: ")
            while chosen_user not in current_users:
                os.system('clear')
                print("Choose an existing user.")
                print("Available Users: ", current_users)
                chosen_user = input("Whose profile do you want to view?: ")
            os.system('clear')
            print('Your Profile: \n')
            labels = ['Name', 'Username', 'Followers']
            with shelve.open('followers') as f:
                selfvars = [users[chosen_user].name, users[chosen_user].username, len(f[chosen_user])]
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
        with shelve.open('posts') as posts:
            post = Message(self.username)
            posts['all_users'].append(post)
            posts[self.username].append(post)

    def delete_post(self):
        os.system('clear')
        print('Delete Post: \n')
        with shelve.open('posts') as posts:
            for index, post in enumerate(posts[self.username]):
                print('{0}: {1}'.format((index+1), post.message))
            n = int(input("\nWhich would you like to delete? [enter int]: ")) - 1
            running = True
            selected_message = ''
            while running:
                try:
                    selected_message = posts[self.username][n].message
                    posts[self.username].pop(n)
                except:
                    print("You must enter an acceptable answer.")
                    n = int(input("Which would you like to delete? [enter int]: ")) - 1
            del_indexes = []
            for index, post in enumerate(posts['all_users']):
                if post.message == selected_message and post.user == self.username:
                    del_indexes.append(index) #in case there is more than one message with the same content by the same user... very special edge case
            for index in range(del_indexes[-1], del_indexes[0]):
                #i reversed the list in case removing a message changes the index values of the items behind it... not sure if it does :/
                posts['all_users'].pop(index)

    def view_posts(self): #view all posts by all users
        os.system('clear')
        print('View Wall: \n')
        with shelve.open('posts') as posts:
            if len(posts['all_users']) == 0:
                for post in posts['all_users']:
                    if post.user not in current_users:
                        print("{0}: {1}".format('[deleted]',post.message))
                    else:
                        print("{0}: {1}".format(post.user,post.message))
                    time.sleep(1)
                    print('here')
            else:
                print("There are no posts yet.")

    def send_message(self):
        with shelve.open('inboxes') as i:
            os.system('clear')
            print('Send A Message: \n')
            if len(current_users) == 1: #need a different user for this function
                print("There are no other users :(")
            else:
                current_users.remove(self.username)
                print('Available Users: ', current_users)
                n = input("Who do you want to send your message to? (enter a username): ")
                #making sure the user picks an existing username that is not their own
                if n in current_users:
                    user = n
                else:
                    while n not in current_users:
                        os.system('clear')
                        print('Available Users: ', current_users)
                        n = input("Who do you want to send your message to? (enter a username): ")
                    user = n
                message = Message(self.name)
                i[user].append(message)
                current_users.append(self.username)

    def view_inbox(self):
        with shelve.open('inboxes') as i:
            os.system('clear')
            print('View Inbox: \n')
            #goes through every message
            if len(i[self.username]) == 0:
                print('There is nothing here :/')
            else:
                for message in i[self.username]:
                    print("From {0}: {1}".format(message.user,message.message))
                    time.sleep(1.5)
                i[self.username] = []

    def follow_user(self):
        running = True
        while running:
            with shelve.open('users') as users:
                os.system('clear')
                print('Follow A User: \n')
                if self.username in current_users:
                    current_users.remove(self.username)
                for user in current_users: #removes any users that the current user already follows
                    print('user', user)
                    with shelve.open('followers') as f:
                        if self.username in f[user]:
                            current_users.remove(user)
                if len(current_users) == 0: #need another user for this function
                    print("There are no other users :(")
                    running = False
                else:
                    print('Available Users: ', current_users)
                    n = input("Who do you want to follow? (enter a username): ")
                    #making sure the user picks an existing username that is not their own
                    if n in current_users:
                        user = n
                    else:
                        while n not in current_users:
                            os.system('clear')
                            print('Available Users: ', current_users)
                            n = input("Who do you want to follow? (enter a username): ")
                        user = n
                    with shelve.open('followers') as f:
                        f[user].append(self.username)
                    with shelve.open('followers') as f:
                        print('user', user, 'followers', f[user])
                    n = input("Do you want to follow another user? (y/n): ")
                    if n != 'y': #try again -- don't really care if the human doesn't input correct response... they will answer 'y' if they want to try again
                        running = False
                    else:
                        current_users.remove(user)

    def delete_user(self):
        with shelve.open('users') as users:
            users[self.username] = []
        get_current_users()
        with shelve.open('followers') as f:
            f[self.username] = []
        with shelve.open('inboxes') as i:
            i[self.username] = []

def program(user): #USER DASHBOARD
    os.system('clear')
    logged_in_menu = Menu(2, user)
    while logged_in_menu.response != 10: #keeps the program running while user is logged in
        response = logged_in_menu.response
        get_current_users()
        if response == 1: #profile
            user.view_profile()
        elif response == 2: #edit
            user.edit_creds()
        elif response == 3: #post
            user.new_post()
        elif response == 4: #delete
            user.delete_post()
        elif response == 5: #wall
            user.view_posts()
        elif response == 6: #message
            user.send_message()
        elif response == 7: #inbox
            user.view_inbox()
        elif response == 8: #follow
            user.follow_user()
        elif response == 9: #user
            user.delete_user()
            break
        input('\npress [enter] to go back to menu') #stops content from being erased too quickly
        logged_in_menu = Menu(2, user)
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
        os.system('clear')
        print('Menu Choices: ')
        print(menu_1_text)
        n = int(input("What do you want to do? (1/2/3): "))
        while n > 3 or n < 1: #ensures available options are chosen
            os.system('clear')
            print('Menu Choices: ')
            print(menu_1_text)
            n = int(input("What do you want to do? (1/2/3): "))
        self.response = n
    def program_menu(self): #user dashboard menu
        os.system('clear')
        print("{0}'s Dashboard: ".format(self.user.username))
        print(menu_2_text)
        n = int(input("What do you want to do? (1/.../10): "))
        while n > 10 or n < 1: #ensures available options are chosen
            os.system('clear')
            print("{0}'s Dashboard: ".format(self.user.username))
            print(menu_2_text)
            n = int(input("What do you want to do? (1/.../10): "))
        self.response = n

def login(): #LOGIN FUNCTION
    with shelve.open('users') as users:
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
            return [chosen_user, False]
        chosen_pass = hash(getpass.getpass("Password: "))
        while chosen_pass != users[chosen_user].password and chosen_pass != hash(admin_passkey):
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
                return [chosen_user, False]
        return [chosen_user, True]

def main():
    print("Welcome to Pinsta!")
    time.sleep(2.5)
    first_menu_choice = Menu(1)
    while first_menu_choice.response != 3:
        with shelve.open('users') as users:
            get_current_users()
            #LOG INTO PROGRAM
            if first_menu_choice.response == 1:
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