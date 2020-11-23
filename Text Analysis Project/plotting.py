import matplotlib.pyplot as plt

<<<<<<< HEAD
def plot_guesses_graph(x_vals, y_vals, max_y, axis_names):
=======
#made my own camelcase function
def camelcase(word):
	s = "".join(word[0].upper() + word[1:].lower())
	return s

#plotting the line graph
def plot_guesses_graph(x_vals, y_vals, axis_names):
>>>>>>> 1c37c1dfc3e80c0edc6a528089d305237b5cd01b
	fig, ax = plt.subplots(1,1)
	ax.plot(x_vals, y_vals)
	ax.set_xlabel("count number")
	ax.set_ylabel("guess value")
	ax.set_title("Your Guesses")
	plt.show()

<<<<<<< HEAD
	print("You are here")

def plot_word_freqs_graph(freqs):
	# Pie chart, where the slices will be ordered and plotted counter-clockwise:
	labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
	sizes = [15, 30, 45, 10]
	explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
			shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

=======
#tranforms the frequency dictionary to a sorted list
def freq_to_list(freqs):
	freq_list = []
	for freq in freqs:
		freq_list.append([freqs[freq], freq])
	return sorted(freq_list, reverse=True)

#function to run loops to get necessary pie slice labels and percentages
def pie_chart_word_info(sort_freqs):
	sizes, labels = [], []
	other_count = 0
	for freq in sort_freqs:
		#made it 20 because lower numbers caused the pie chart to become cramped
		if freq[0] > 20:
			sizes.append(freq[0])
			labels.append(freq[1])
		else:
			other_count += 1
	#if the frequency is lower than 20
	if len(sizes) == 0:
		for x in range(5):
			sizes.append(sort_freqs[x][0])
			labels.append(sort_freqs[x][1])
			other_count -= 1
	return sizes, labels, other_count

def pie_chart_letter_info(letter_list):
	sizes, labels = [], []
	other_count = 0
	for pair in letter_list:
		if pair in letter_list[:5]:
			sizes.append(pair[0])
			labels.append(pair[1])
			other_count -= 1
		other_count += 1
	return sizes, labels, other_count

def plot_pie_chart(freqs, letters, file_name, mode):
	#pie chart set up
	if mode == "word":
		sorted_freqs = freq_to_list(freqs)
		sizes, labels, other_count = pie_chart_word_info(sorted_freqs)
	else:
		sizes, labels, other_count = pie_chart_letter_info(letters)
	sizes.append(other_count)
	labels.append('other')

	#pie chart configurations
	fig1, ax1 = plt.subplots()
	#sets percents to show one decimal
	ax1.pie(sizes, labels=sizes, autopct='%1.1f%%')
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	ax1.set_title("{0} Frequencies within the file {1}".format(camelcase(mode), file_name))
	#gives legend to make it easier for user to understand
	ax1.legend(labels, loc='best')
>>>>>>> 1c37c1dfc3e80c0edc6a528089d305237b5cd01b
	plt.show()