<<<<<<< HEAD
import analysis, random, plotting, os

urls = ['https://www.w3.org/TR/PNG/iso_8859-1.txt']
files = ['Text\ Analysis\ Project/gettysburg.txt', 'Text\ Analysis\ Project/hippocraticoath.txt']
=======
import analysis, replit, random, plotting

urls = ['https://www.w3.org/TR/PNG/iso_8859-1.txt'] #web page
files = ['gettysburg.txt', 'hippocraticoath.txt'] #txt files
>>>>>>> 1c37c1dfc3e80c0edc6a528089d305237b5cd01b

#choosing the text file / url
if random.randint(0, 1) == 1:
	url = random.choice(urls)
	print(url)
	data = analysis.get_web_text(url)
<<<<<<< HEAD
else:
	file_name = random.choice(files)
	print(file_name)
	data = analysis.get_file_text(file_name)
print(data)

#setting up the text files
sentences = analysis.get_sentences(data)
cleaned_sentences = analysis.clean(sentences)
words = analysis.get_words(sentences)
print(words)
word_freqs = analysis.get_freqs(words)
os.system('clear')
print("---------------")

#setting up the game
secret_word = random.choice(words)
secret_answer = word_freqs[secret_word]
running = False
=======
	file_name = 'Graphical Characters'
else:
	url = random.choice(files)
	data = analysis.get_file_text(url)
	if url == "gettysburg.txt":
		file_name = 'Gettysburg Address'
	else:
		file_name = 'Hippocratic Oath'

#setting up the text files
sentences = analysis.get_sentences(data)
words = analysis.get_words(sentences)
words = analysis.clean(words)
#if gamemode is words
word_freqs = analysis.get_word_freqs(words)
#if gamemode is letters
letters = analysis.get_letter_freqs(words)
replit.clear()
print("---------------")

#determine gamemode
modes = ['word', 'letter']
gamemode = random.choice(modes)
print(gamemode)

#setting up the game
if gamemode == "word":
	secret_word = random.choice(words)
	secret_answer = word_freqs[secret_word]
else:
	secret_word = random.choice(letters)
	secret_answer = secret_word[0]
	secret_word = secret_word[1]
running = True
>>>>>>> 1c37c1dfc3e80c0edc6a528089d305237b5cd01b
guesses = [0]
count = 0
counts = [0]

#playing the game
while running:
<<<<<<< HEAD
	user_guess = int(input("How many times do you think the word '{0}' is in {1}?: ".format(secret_word, url)))
=======
	#dynamic input so I don't have two different while loops
	user_guess = int(input("How many times do you think the {0} '{1}' is in the {2} file?: ".format(gamemode, secret_word, file_name)))
>>>>>>> 1c37c1dfc3e80c0edc6a528089d305237b5cd01b
	guesses.append(user_guess)
	count += 1
	counts.append(count)
	if(user_guess > secret_answer):
		print("Too high!")
	elif(user_guess < secret_answer):
		print("Too low")
	else:
		print("Yay! You got it!")
		running = False
<<<<<<< HEAD
	# update the graph here? maybe cannot
	print(counts, guesses)
=======
>>>>>>> 1c37c1dfc3e80c0edc6a528089d305237b5cd01b

#plotting my graph
answer = input("Line graph or a pie chart? (l/p): ")
while answer != "l" or answer != "p":
	if answer == "l" or answer == "p":
		break
	answer = input("Line graph or a pie chart? (l/p): ")
<<<<<<< HEAD
if answer == "l":
	maximum = 0
	for guess in guesses:
		if guess > maximum: maximum = guess
	plotting.plot_guesses_graph(counts, guesses, maximum, ["guess_num", "guess_val"])
else:
	plotting.plot_word_freqs_graph(word_freqs)

'''
TO DO LIST
- maybe track how hard it was? (something about percentages and stuff)
	- based upon probability of picking the word (freq of word / count of all words)
- show a pie chart of freqs of words?
=======
if answer == "l": #line graph
	plotting.plot_guesses_graph(counts, guesses, ["guess_num", "guess_val"])
else: #pie chart
	plotting.plot_pie_chart(word_freqs, letters, file_name, gamemode)

'''
TO DO LIST
>>>>>>> 1c37c1dfc3e80c0edc6a528089d305237b5cd01b
- "ya like jazz?" -- bee movie
'''