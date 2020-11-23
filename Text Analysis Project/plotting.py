import matplotlib.pyplot as plt

def plot_guesses_graph(x_vals, y_vals, max_y, axis_names):
	fig, ax = plt.subplots(1,1)
	ax.plot(x_vals, y_vals)
	ax.set_xlabel("count number")
	ax.set_ylabel("guess value")
	ax.set_title("Your Guesses")
	plt.show()

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

	plt.show()