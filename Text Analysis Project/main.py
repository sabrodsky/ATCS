import analysis, random, plotting, os

urls = ['https://www.w3.org/TR/PNG/iso_8859-1.txt']
files = ['Text\ Analysis\ Project/gettysburg.txt', 'Text\ Analysis\ Project/hippocraticoath.txt']

#choosing the text file / url
if random.randint(0, 1) == 1:
	url = random.choice(urls)
	print(url)
	data = analysis.get_web_text(url)
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
guesses = [0]
count = 0
counts = [0]

#playing the game
while running:
	user_guess = int(input("How many times do you think the word '{0}' is in {1}?: ".format(secret_word, url)))
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
	# update the graph here? maybe cannot
	print(counts, guesses)

#plotting my graph
answer = input("Line graph or a pie chart? (l/p): ")
while answer != "l" or answer != "p":
	if answer == "l" or answer == "p":
		break
	answer = input("Line graph or a pie chart? (l/p): ")
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
- "ya like jazz?" -- bee movie
'''