import urllib.request

def get_web_text(url):
	data = urllib.request.urlopen(url)
	encoded = data.read()
	decoded = encoded.decode('utf-8')
	return decoded

def get_file_text(file_name):
<<<<<<< HEAD
	data = open(file_name).readlines()
=======
	data = open(file_name).read()
>>>>>>> 1c37c1dfc3e80c0edc6a528089d305237b5cd01b
	return data

def get_sentences(file):
	line_list = []
	for line in file.split("."):
		if line != "\n":
			line_list.append(line) #removes paragraph breaks
	return line_list

<<<<<<< HEAD
def clean(text):
	cleaned_list = []
	punctuation = ['.', ',', '(', ')', '-', '/', "'", '"', '&']
	for word in text:
		#replacing all line breaks with nothing
		word1 = word.replace('\n', '')
		for punct in punctuation:
			if punct in word1:
				word1 = word1.replace(punct, '')
		cleaned_list.append(word1)
=======
#removes unwanted stuff and only keeps the allowed characters
def clean(words):
	cleaned_list = []
	allowed = "abcdefghijklmnopqrstuvwxyz01234567890"
	for word in words:
		word_string = word.replace('\n', '')
		empty_string = ""
		for char in word_string:
			if char in allowed:
				empty_string += char
		cleaned_list.append(empty_string)
>>>>>>> 1c37c1dfc3e80c0edc6a528089d305237b5cd01b
	return cleaned_list

def get_words(lines):
	words = []
	for line in lines:
		for word in line.split():
			words.append(word.lower())
	return words

<<<<<<< HEAD
def get_freqs(words):
=======
def get_word_freqs(words):
>>>>>>> 1c37c1dfc3e80c0edc6a528089d305237b5cd01b
	freqs = {}
	for word in words:
		if word in freqs.keys():
			freqs[word] += 1
		else:
			freqs[word] = 1
<<<<<<< HEAD
	return freqs
=======
	return freqs

def get_letter_freqs(words):
	freqs = {}
	freqs_list = []
	for word in words:
		word = word.lower()
		if word.isalpha(): #checks if word is only letters
			for char in word:
				if char in freqs.keys():
					freqs[char] += 1
				else:
					freqs[char] = 1
	for freq in freqs:
		freqs_list.append([freqs[freq], freq])
	return sorted(freqs_list, reverse=True)
>>>>>>> 1c37c1dfc3e80c0edc6a528089d305237b5cd01b
