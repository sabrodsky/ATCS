import random

def choose_word():
	words = open("Hangman/words.txt").readlines()
	myword = random.choice(words)
	return (myword.strip())

def display_word(word,chosen):
	#show the word in its current state including blanks for letters not chosen.
	display_string = ""

	for i in range(0,len(word)):
		if(word[i] in chosen):
			display_string += word[i] + " "
		else:
			display_string += "_ "

	return display_string

def handle_guess(word):
	#get the guess, update chosen, give feedback to user such as -- you are correct
	letter = input("guess a letter: ")
	if len(letter) == 1:
		if letter in word:
			print("correct")
			print("")
		else:
			print("incorrect")
			print("")
	else:
		print("You can only guess one letter at a time")

	return letter[0]

def game_status(word,chosen):
	#show graphics & chosen letters
	wrongCounter = 0
	for letter in chosen:
		if letter not in word:
			wrongCounter+= 1
	won = True
	for letter in word:
		if letter not in chosen:
			won = False
	if wrongCounter >= 7:
		print("You lost :(")
		show_hangman(wrongCounter)
		return True
	elif won:
		print("You Won!")
		show_hangman(wrongCounter)
		return True
	else:
		show_hangman(wrongCounter)
		print("Already guessed:",chosen)
		return False
	#announce the outcome if the game is over
	#return boolean of whether the game is over.

def show_hangman(wrongCounter):
	print("   --- ")
	if wrongCounter >= 1:
		print("   O  |")
	else:
		print("      |")
	if wrongCounter >= 2:
		if wrongCounter >= 3:
			if wrongCounter >= 4:
				print("  /|\ |")
			else:
				print("  /|  |")
		else:
			print("  /   |")
	else:
		print("      |")
	if wrongCounter >= 5:
		print("   |  |")
	else:
		print("      |")
	if wrongCounter >= 6:
		if wrongCounter >= 7:
			print("  / \ |")
		else:
			print("  /   |")
	else:
		print("      |")

def main():
	game_over = False
	secret_word = choose_word()
	chosen_letters = ""
	while game_over == False:
		print(display_word(secret_word, chosen_letters))
		chosen_letters += handle_guess(secret_word)
		game_over = game_status(secret_word, chosen_letters)
	print("The word was: " + secret_word)
main() 