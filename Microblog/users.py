def get_cur_usernames():
    current_usernames = []

    users = open('users.txt', 'r')
    for index, line in enumerate(users.readlines()):
        username = line[line.find('/')+2:line.rfind('/')-1]
        if username != "Username":
            current_usernames.append(username)
    return current_usernames