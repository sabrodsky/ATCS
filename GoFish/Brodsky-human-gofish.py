import random, os, time

def determine_num_players(): #determines how many human players are in the game
	n = int(input("How many players? (2-7): "))
	if(n >= 2 and n <= 7):
		player_num = n
	else:
		print("The number of players must be between 2 and 7")
		player_num, hand_card_num = determine_num_players()
	return player_num, 7 #default is 7

def create_deck(): #generates a new deck
	deck = []
	for x in range(4): #note: I don't pay any attention to the suit as Go Fish only needs the card value
		for y in range(13): #adds 4 of each card value
			deck.append(y + 1)
	# print(deck)
	return deck

def deal_hand(deck, num_cards, players):
	# deals multiple cards from the deck. The cards are returned as a list that represents the hand drawn and they are removed from the deck
	hands = {}
	for x in range(players): #creates a dictionary depending on how many players are playing the game
		hands[x + 1] = []
	for x in range(num_cards * players): 
		hands[(x%players)+1].append(deck[0]) #runs through the deck (deals one card to one player at a time rather than all card to one player, then all cards to another player)
		deck.pop(0)
	return hands, deck

def create_trick_booklet(players): #creates a trick booklet depending on how many players are in the game
	book = {}
	for x in range(players):
		book[x+1] = []
	return book

def hand_in_card(hand_decks, cur_player, card_value): #checks if a card is in a player's hand
	for x in range(len(hand_decks[cur_player])):
			if(int(hand_decks[cur_player][x]) == card_value):
				return True
	return False

def choose_a_card_value(): #handle_guess() asks user what card value they want to steal
	m = input("Which card? (1-13): ")
	if(m.isnumeric()):
		n = int(m)
		if(n <= 13 and n >= 1):
			x = n
		else:
			print("The card must have a value between 1 and 13!")
			x = choose_a_card_value()
	else:
		print("You must input a number!")
		x = choose_a_card_value()
	return x

def choose_a_player(players, cur_player): #handle_guess() asks user from which player they want to steal
	m = input("Which player? (1/2/3/...): ")
	if(m.isnumeric()):
		n = int(m)
		if(n == cur_player):
			print("You cannot choose yourself!")
			x = choose_a_player(players, cur_player)
		if(n <= players and n >= 1):
			x = n
		else:
			print("The selected player must be between 1 and {0}!".format(players)) #makes sure the user picks a playing player
			x = choose_a_player(players, cur_player)
	else:
		print("You must input a number!") #makes sure the user picks a playing player
		x = choose_a_player(players, cur_player)
	return x

def go_fish(deck_pile, hand_decks, cur_player): #adds a card from the deck into the player's hand
	print("GO FISH")
	if(len(deck_pile) > 0):
		random.shuffle(deck_pile)
		hand_decks[cur_player].append(deck_pile[0])
		deck_pile.pop(0)
	else:
		print("No more cards in the deck! :(")
	return hand_decks, deck_pile

def check_tricks(cur_player, hand_decks, player_tricks): #runs through player hand to see if there are any available tricks
	card_freq = check_freq(hand_decks[cur_player])
	for x in range(len(card_freq)):
		if(card_freq[x][1] == 4): #needs to have four of the same values to be a trick
			player_tricks[cur_player].append(card_freq[x][0]) #adds the value to the trick booklet
			remove_card = card_freq[x][0]
			for z in range(4):
				hand_decks[cur_player].remove(remove_card) #removes all values from the trick 
	return hand_decks, player_tricks

def shuffle_deck(deck): #uses random to shuffle the deck
	random.shuffle(deck)
	return deck

def check_freq(hand): #checks and returns frequencies within player hand
	freqs = {}
	for card in hand: #first makes a dictionary of card values and their frequencies
		if card in freqs:
			freqs[card] += 1
		else:
			freqs[card] = 1
	freqs_list = []
	for key in freqs: #puts into a list
		freqs_list.append([key, freqs[key]])
	return sorted(freqs_list)

def check_hand_length(players, hand_decks): #checks the length of all hands
	hand_lengths = {}
	for x in range(players):
		hand_lengths[x+1] = str(len(hand_decks[x+1])) + " cards"
	return hand_lengths

def check_game_status(player_tricks, players): #ends the game if the trick booklet has 13 tricks
	count_tricks = 0
	for x in range(players):
		count_tricks += len(player_tricks[x+1])
	if(count_tricks == 13):
		return False
	else:
		return True

def handle_guess(cur_player, hand_decks, deck_pile, players, book_of_tricks): #handles human and AI guesses
	turnRunning = True
	while turnRunning and len(hand_decks[cur_player]) > 0:
		print("It is currently Player {0}'s turn".format(cur_player))
		player_chosen = choose_a_player(players, cur_player)
		card_val_chosen = choose_a_card_value()
		has_card_val = hand_in_card(hand_decks, cur_player, card_val_chosen) #makes sure the user has card in their hand
		stolen_cards = []
		if(has_card_val):
			for x in range(len(hand_decks[player_chosen])): #goes through selected player's hand and takes any matching card values out
				if(hand_decks[player_chosen][x] == card_val_chosen):
					stolen_cards.append(hand_decks[player_chosen][x])
			for x in range(len(stolen_cards)): #removes stolen cards from selected player and puts them into user's hand
				hand_decks[player_chosen].remove(card_val_chosen)
				hand_decks[cur_player].append(stolen_cards[x])
		else: #has user pick another card (and I guess another player if they want) -- wouldn't happen to AI so...
			print("You must pick a card in your hand!")
			hand_decks, deck_pile = handle_guess(cur_player, hand_decks, deck_pile, players, book_of_tricks)
			break
		os.system('clear')
		if(len(stolen_cards) == 0): #if their attempts failed, goes to go_fish function and end the turn
			hand_decks, deck_pile = go_fish(deck_pile, hand_decks, cur_player)
			turnRunning = False
		else: #otherwise the player gets to take another turn
			print("YOU GOT IT!")
		print("Player {0}: ".format(cur_player) + str(sorted(hand_decks[cur_player])))
		hand_decks, book_of_tricks = check_tricks(cur_player, hand_decks, book_of_tricks) #checks to see if the has ended
		input("Current Tricks: " + str(book_of_tricks) + " [press ENTER]")
	return hand_decks, deck_pile

def check_winner(player_tricks, players): #player who has most tricks win the game
	winner = 1
	winners = [winner]
	for x in range(players):
		if(len(player_tricks[x+1]) > len(player_tricks[winner])):
			winner = (x+1)
			winners = [winner]
		elif(len(player_tricks[x+1]) == len(player_tricks[winner])): #each value is the number of tricks earned
			winners.append(x+1)
	return winners

def prompt_play_again(): #asks user if they want to play again
	n = input("Would you like to play again? (y/n): ")
	if(n == "y"):
		x = True 
	elif(n == "n"):
		x = False
	else:
		print("That is not an answer!")
		x = prompt_play_again()
	os.system('clear')
	return x

def main():
	#lots of setup for the game
	gameRunning = True
	players, hand_card_num = determine_num_players()
	new_deck = create_deck()
	shuffle_deck(new_deck)
	hand_decks, deck_pile = deal_hand(new_deck, hand_card_num, players)
	book_of_tricks = create_trick_booklet(players)
	#game loop
	while(gameRunning):
		for x in range(players):
			os.system('clear')
			gameRunning = check_game_status(book_of_tricks, players)
			if(not gameRunning): #ends the game if the game should end
				break
			current_player = int(x + 1)
			if(len(hand_decks[current_player]) > 0 or len(deck_pile) > 0): #if a user has no more cards in their hand or if the deck has no cards
				if(len(hand_decks[current_player]) == 0): #if they have no cards, pick another card from deck
					hand_decks[current_player].append(deck_pile[0])
					deck_pile.pop(0)
				input("Turn to player {0}: ".format(x + 1) + " [press ENTER]") #alerts players whose turn it is
				os.system('clear')
				print("Hand Lengths: " + str(check_hand_length(players, hand_decks))) #prints hand lengths
				print("Your Hand: " + str(sorted(hand_decks[current_player]))) #prints user's hand
				hand_decks, deck_pile = handle_guess(current_player, hand_decks, deck_pile, players, book_of_tricks) #human + AI players make a guess
				time.sleep(5) #lets users see their new hand before moving on to another player
			else: #if the player cannot pick another card from the deck and has no cards, they cannot take any turns
				print("Player {0} cannot go... :(".format(current_player))
	#prints out the winners of the game
	winner = check_winner(book_of_tricks, players)
	if len(winner) == 1:
		print("Winner: Player {0}!".format(winner[0]))
	else:
		print("Tie between Players {0}!".format(winner))
	
	if(prompt_play_again()):
		main() #resets everything
	else:
		print("Game Over") #ends the game
main()