import urllib.request

def get_web_text(url):
	data = urllib.request.urlopen(url)
	encoded = data.read()
	decoded = encoded.decode('utf-8')
	return decoded

def get_file_text(file_name):
	data = open(file_name).readlines()
	return data

def get_sentences(file):
	line_list = []
	for line in file.split("."):
		if line != "\n":
			line_list.append(line) #removes paragraph breaks
	return line_list

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
	return cleaned_list

def get_words(lines):
	words = []
	for line in lines:
		for word in line.split():
			words.append(word.lower())
	return words

def get_freqs(words):
	freqs = {}
	for word in words:
		if word in freqs.keys():
			freqs[word] += 1
		else:
			freqs[word] = 1
	return freqs