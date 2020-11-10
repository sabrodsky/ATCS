import random, os, time

def determine_game(): #choose if it's one-player or two-player
	n = input("One-player or two-player? (1/2): ")
	if(n == "1"):
		x = 1
	elif(n == "2"):
		x = 2
	else:
		print("That is not an answer!")
		x = determine_game()
	return x

def choose_gamemode(): #single-player difficulty selection
	os.system('clear')
	n = input("Would you like easy, medium, hard, or impossible? (e/m/h/i): ")
	if(n == "e"):
		gamemode = "easy"
	elif(n == "m"):
		gamemode = "medium"
	elif(n == "h"):
		gamemode = "hard"
	elif(n == "i"):
		gamemode = "impossible"
	else:
		print("That is not an answer!")
		gamemode = choose_gamemode()
	return gamemode

def question1(): #two-player chooses if they want custom answer or computer-generated answer
	n = input("Would you like to use a computer-generated answer or write your own? (c/o): ")
	if(n == "c"):
		x = "computer"
	elif(n == "o"):
		x = "own"
	else:
		print("That is not an answer!")
		x = question1()
	return x

def choose_answer(mode): #function for computer-generated answer
	words = open("Hangman/words.txt").readlines()
	medium_phrases = open("Hangman/3-6phrases.txt").readlines()
	hard_phrases = open("Hangman/7-10phrases.txt").readlines()
	answer_string = ""
	if(mode == "easy"):
		guesses = 8
		myword = random.choice(words)
		answer_string += myword.strip()
	elif(mode == "medium"):
		choice = random.randint(0, 1)
		if(choice == 0): #answer is a word
			guesses = 6
			answer_string += random.choice(words).strip()
		else: #answer is a short phrase
			guesses = 8
			answer_string = random.choice(medium_phrases).strip()
	elif(mode == "hard"): #answer is longer phrase
		guesses = 8
		answer_string = random.choice(hard_phrases).strip()
	else: #answer is a string of random words of a random length
		guesses = 6
		for x in range(random.randint(1, 10)):
			answer_string += random.choice(words).strip() + " "
	return [answer_string.lower(), guesses]

def player_answer(): #user inputs their custom answer
	os.system('clear')
	input("Player One, turn the screen away from Player Two! (press ENTER): ")
	os.system('clear')
	answer = input("Player One, type in a word or a phrase: ")
	guesses = int(input("Player One, how many guesses should Player Two receive?: "))
	os.system('clear')
	return answer, guesses

def determine_height_limit(answer): #determining the height limit
	letters = []
	for x in range(len(answer)): #counting how many individual letters there are in the answer string
		if(answer[x] not in letters and answer[x] != " "):
			letters.append(answer[x])
	
	limit = len(letters) - int(len(letters)/len(answer.split())) #the famed formula
	return limit

def display_word(answer,chosen): #show the word in its current state
	display_string = ""

	for i in range(0,len(answer)):
		if(answer[i] in chosen and answer[i] != " "):
			display_string += answer[i] + " " #displays letter
		elif(answer[i] == " "):
			display_string += "/ " #indicates a space within the phrase
		else:
			display_string += "_ " #indicates a missing letter

	return display_string

def draw_flyguy(changeY, altitude, height_limit): #show user their progress to either saving rocket or crashing rocket
	altitude += changeY
	for x in range(height_limit):
		if(x == (height_limit - (altitude))): print("_ \N{rocket}") #determining position of the rocket
		else: print("_")
		if(x == (height_limit - 1)): print("_________________________") #printing the ground
	print("altitude: " + str(altitude))
	time.sleep(3)
	return altitude

def handle_guess(answer, guesses, chosen, correct): #tells user if their guess is correct or wrong
	if(len(chosen) == 1):
		print("You haven't guessed any letters")
	else:
		print("\nGuessed Letters: " + chosen)
	n = input("Guess a letter: ")
	if(n in answer and n not in chosen):
		print("Correct!")
		if(correct < 0):
			correct = 0
		else:
			correct = 1
		chosen += n
	elif(n in chosen):
		print("You have already guessed this letter!")
		return guesses, chosen, correct
	else:
		print("Wrong!")
		guesses -= 1
		if(correct > 0):
			correct = 0
		else:
			correct = -1
		chosen += n
	
	return guesses, chosen, correct

def game_status(answer, chosen, guesses, altitude, height_limit): #runs tests to see if the game should end or continue
	if(guesses == 0): #ran out of guesses
		print("You lost!")
		return True
	if(altitude == height_limit): #user has reached height_limit
		return True
	if(altitude == 0):
		return True
	for x in range(len(answer)): #checking if all of the letters in answer have been guessed
		if(answer[x] not in chosen):
			return False #if there is a letter in answer that hasn't been guessed, the game continues
	return True

def main(): #the main game function
	os.system('clear')
	print("""
	Welcome to Flyguy!

	In this game, there are four different modes. To play this game, you must guess the correct answer.
	Your character is a rocket (\N{rocket}) icon.

	To win, you must guess the answer before your rocket crashes into the ground.
	To gain altitude, you must guess correctly.
	But you can also lose altitude! If you answer incorrectly, the rocket gets closer to the ground :(
	When the rocket crashes into the ground, you lose.

	Now, you can either play with a computer or with another person.
	""") #printing info for user
	mode = determine_game()
	correct = 0
	game_over = False
	print("""
	Now you must pick the difficulty!

	Easy: the answer is just a single word and you have eight guesses.
	Medium: the answer is either a word or a short phrase (3-6 words). You have six guesses if it's a word and eight if it's a phrase.
	Hard: the answer is a long phrase (7-10 words) and you have eight guesses.
	Impossible: the answer is a random string of words of a random length and you have six guesses.
	""") #printing info for user
	if(mode == 1):
		gamemode = choose_gamemode() #user chooses a gamemode
		answer, guesses = choose_answer(gamemode) #the game chooses an answer
	else:
		answer1,gamemode = question1()
		if(answer1 == "computer"):
			answer, guesses = choose_answer(gamemode)
		else:
			answer, guesses = player_answer() #user chooses the answer
	og_guesses = guesses
	altitude = int(guesses/2)
	height_limit = determine_height_limit(answer) #determines height limit
	chosen_letters = " "
	while game_over == False:
		os.system('clear')
		print(display_word(answer, chosen_letters)) #tells user which letters are correct and how many are left
		guesses, chosen_letters, correct = handle_guess(answer, guesses, chosen_letters, correct) #tells user if their guess is correct
		altitude = draw_flyguy(correct, altitude, height_limit) #displays the character
		game_over = game_status(answer, chosen_letters, guesses, altitude, height_limit) #checks if game is over or still running
		time.sleep(1)
	os.system('clear')
	if(altitude > 0):
		print("YOU WIN! \N{parachute}")
	else:
		print("YOU LOST! \N{skull and crossbones}")
	print("The answer was: " + answer)
main()