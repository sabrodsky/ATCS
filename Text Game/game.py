import random, time, os, shelve, math, textwrap

# THERE ARE A LOT OF THINGS IN HERE THAT I DON'T USE... OH WELL

#general, helpful stuff
user_classes = """
|----------------------------------|
|_________| HP values | ATK values |
| peasant |       100 |         50 |
| wizard  |        80 |         80 |
| warrior |        70 |        100 |
| tank    |       150 |         30 |
| gambler |    50~170 |     10~120 |
|----------------------------------|
"""
help_menu = """
	attack (a) [monster]: attack a monster
	backpack (b) [item]: see inside your inventory OR see current quantity of an item
	consume (c) [item]: drink item or eat food
	discard (d) [item]: throw an item away
	erase (e): clears the command line
	go (g) [scene]: go to a scene
	help (h): view the help menu
	interact (i) [item]: interact with an object
	look (l) [item]: see an object's function
	map (m): see the scenes
	open (o) [item]: open up something (ie. chest, door, window)
	profile (p): view user profile
	scan (s): scans the room for interactable objects
	unlock (u) [item]: unlock something by using up one key
"""

#general, helpful functions
specimen_num = random.randint(1, 9999)
def db_init():
	with shelve.open('game') as g:
		g['user_stats'] = {} #will store user object [key == username, value == object]
		g['shop'] = {'inventory': {}, 'probability': 100} #will store current shop inventory (and probability of a restock)
		g['user_progress'] = {} #will store user progress [key == username, value == object]
def title(title):
	os.system('clear')
	print('{}: \n'.format(title))
def clear(t=0):
	time.sleep(t)
	os.system('clear')
def cont():
	input("\n press [enter] to continue ")
def path_picker():
	print("would you like to go to the jungle or the tundra?")
	n = input("[jungle/tundra]> ").lower()
	while n != 'jungle' and n != 'tundra':
		print("enter 'jungle' or 'tundra'")
		print("would you like to go to the jungle or the tundra?")
		n = input("[jungle/tundra]> ").lower()
	if n == 'jungle':
		new_map.jungle = True
		return ''
	else:
		new_map.tundra = True
		return 'polaris'
def book_picker(scene):
	book_responses = [
		'the book was exciting... yay',
		'you fell asleep while reading the book... oh well',
		'you slowly made your way through the book. you were unhappy, but still wanted to know what happened at the end...'
	]
	print("Books:\n")
	for book in Basement.books:
		print("[-] {}".format(book))
	book = input("[book title]> ")
	while book not in Basement.books:
		print("enter a book title")
		book = input("[book title]> ")
	if book == 'The Lion, the Witch, and the Wardrobe':
		scene.open_portal = True
		print("you try to take out the book, but it holds still. you try again, this time pulling from the top of the book. to your surprise, the book moves like a lever and you hear a click. you slide the bookcase to the side, revealing a portal.")
	else:
		print(random.choice(book_responses))
def intro():
	clear()
	print("Welcome to The Wanderer!")
	clear(3)

class Monster:
	monsters = ["a land-dwelling octopus", "an evil goblin", "a rabid puppy", "The Devil", 
	"the most evil of ghosts", "a giant blob of slime (his name is Bob)", 
	"a purple alien armed with a futuristic laser gun", "a talking tree", "a zombie", "a flying bear with two swords"]

	def __init__(self, difficulty, name=None):
		if name == None:
			self.name = random.choice(Monster.monsters)
		else:
			self.name = name
		if difficulty == 'easy':
			self.hp = random.randint(1,100)
			self.atk = random.randint(1,5)
			self.reward = [10, 5] #[gold,xp]
		elif difficulty == 'medium':
			self.hp = random.randint(30,150)
			self.atk = random.randint(1,15)
			self.reward = [20, 15] #[gold,xp]
		elif difficulty == 'hard':
			self.hp = random.randint(60,300)
			self.atk = random.randint(1,20)
			self.reward = [30, 30] #[gold,xp]
		else: #boss levels
			self.hp = random.randint(150,300)
			self.atk = random.randint(10,30)
			self.reward = [50, 50] #[gold,xp]

class User:
	classes = ['peasant', 'wizard', 'warrior', 'tank', 'gambler']
	hp = {'peasant': 100, 'wizard': 80, 'warrior': 70, 'tank': 150, 'gambler': random.randint(50, 170), 'god': 10000000000}
	atk = {'peasant': 50, 'wizard': 80, 'warrior': 100, 'tank': 30, 'gambler': random.randint(10, 120), 'god': 10000000000}
	xp_requirement = [100, 100, 100, 100, 100, 150, 150, 150, 175, 175, 200, 200, 250, 250, 300] #total of 15 levels at the moment

	def __init__(self):
		self.inventory = {'apple': 0, 'key': 0}
		self.lvl = 1
		self.xp = 0
		self.gold = 0
		# self.quest = 0
		# self.cur_quest = None
		self.set_name()
		clear(2)
		self.determine_class()
		self.alive = True
	def set_name(self):
		clear()
		print("Create a User: \n")
		self.name = input("[enter name]> ")
	def determine_class(self):
		print("Choose a Class: \n")
		print(user_classes)
		user_class = input("[class name]> ")
		while user_class not in User.hp.keys():
			print("\nenter the name of a class!")
			user_class = input("[class name]> ")
		self.hp = User.hp.get(user_class)
		self.maxhp = self.hp
		self.atk = User.atk.get(user_class)
		print("\nYour hp is {0} and your atk is {1}.".format(self.hp, self.atk))
		clear(5)
	def level_up(self): #run after every xp-gaining activity (battles, 'quests', xp_potions, [other])
		while self.xp >= User.xp_requirement[self.lvl]:
			self.xp -= User.xp_requirement[self.lvl]
			self.lvl += 1
			self.atk *= 1.25
			self.hp *= 1.5
	def get_reward(self, rewards):
		self.gold += rewards[0]
		self.xp += rewards[1]
		self.level_up()
	# def get_quest(self):

class Battle:
	def __init__(self, user, monster):
		self.winner = None
		print("are you sure you want to battle?")
		n = input("[yes/no]> ")
		while n != 'yes' or n != 'no':
			print("enter 'yes' or 'no'")
			print("are you sure you want to battle?")
			n = input("[yes/no]> ")
		if n == 'yes':
			self.start(user, monster)
		else:
			print("you fled from the monster, too scared to fight.")
	def attack(self, player, target):
		print("{0} attacked {1}, dealing {2} damage.".format(player.name, target.name, player.atk))
		target.hp -= player.atk
		print("{0} now has {1} hp.".format(target.name, target.hp))
		if target.hp <= 0:
			self.winner = player
			return False
		else:
			return True
	def start(self, user, monster):
		battle_initiated = True
		clear()
		print("Battle:\n")
		turn = random.randint(0,1) #0 is user; 1 is monster
		while battle_initiated:
			if turn == 0:
				battle_initiated = self.attack(user, monster)
				turn = 1
			else:
				battle_initiated = self.attack(monster, user)
				turn = 0
		if self.winner == user:
			print("You win!")
			user.level_up(monster.reward)
		else:
			user.alive = False

class Scene: #YAY GOTHONS -- teaching me how to use inheritance better :)
	def __init__(self):
		self.title = "example"
		self.prev_scene = None
		self.next_scene = 'death'
		self.visits = 0
		self.repeat_messages = [
			'you entered the scene yet again. nothing has changed.',
			'you walk into the scene, discovering that everything has been destroyed. oh well...'
		]
		self.monsters = {'example': Monster('easy')}
		self.objects = ['door', 'key']

	def play(self, mode='repeat', dialogue="This is here because the author didn't finish yet. Oh well..."):
		if mode == 'repeat':
			print(random.choice(repeat_messages))
		else:
			specimen("""{}""".format(dialogue))

class Bedroom(Scene):
	def __init__(self):
		self.title = "bedroom"
		self.key_found = False
		self.door_unlocked = False
		self.chest_unlocked = False
		self.chest_opened = False
		self.painting_moved = False
		self.objects = ['bed', 'chest', 'door', 'key', 'painting', 'window']
		self.next = 'kitchen'
		self.prev = None
		self.visits = 0
		self.repeat_messages = [
			'You walk into the bedroom and see that everything has been cleaned. Your bed is made, the floor has no clothes, and your windows are no longer dusty. You wonder who could have done this...',
			'You enter your bedroom and everything is the same. The specimen is still hiding in the closet.',
			'The bedroom looks the same, except you understand that everything has been replaced with an exact replica. Well, the specimen is gone so... not everything.'
		]
		self.monsters = {'example': Monster('easy')}
	def play(self, mode='repeat'):
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("You slowly open your eyes, squinting at the bright light shining through your window. You look at your watch, reading that it's 8:07 AM. You get out of bed and get dressed. In your room, there is a chest, a painting, and a window. There is also a key sitting on your bedside table. You walk over to your bedroom door, only to discover that it is locked.")

class Kitchen(Scene):
	def __init__(self):
		self.title = "kitchen"
		self.prev = 'bedroom'
		self.next = 'basement'
		self.visits = 0
		self.repeat_messages = [
			'You walk into the kitchen yet again, wondering why you came back...',
			'You enter the kitchen, hoping to make a grilled cheese sandwich. Sadly you have no cheese so your plans are ruined.',
			'In the kitchen, you open the refrigerator. Inside is a rotten apple and a moldy tin of tomatoes. Too bad.'
		]
		self.objects = ['door', 'chest', 'window', 'painting', 'refrigerator']
		self.refrigerator_unlocked = False
		self.door_unlocked = True
		self.chest_unlocked = False
		self.chest_opened = False
		self.key_found = False
		self.painting_moved = False
		self.monsters = {'example': Monster('easy')}
	def play(self, mode='repeat'):
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("You walk into the kitchen, almost slipping on the slick tile floor. You stand next to the refrigerator, admiring the painting hanging next to the window. Beside the bedroom door, there is another chest.")

class Basement(Scene):
	def __init__(self):
		self.title = "basement"
		self.visits = 0
		self.repeat_messages = [
			'You walk back down into the basement, still in awe it was hidden from you for your entire life.',
			'You start walking down the stairs but accidentally stumble and fall, landing hard on the concrete floor. Ouch.',
			'You rush down the stairs in a hurry. After a few seconds, you stop. Why were you in such a hurry?'
		]
		self.objects = ['chest', 'window', 'sofa', 'bookcase']
		self.open_portal = False
		self.monsters = {'example': Monster('easy')}
		self.books = ['Harry Potter and the Prisoner of Azkaban', 'Moby Dick', 'The Lion, the Witch, and the Wardrobe', 'Winnie the Pooh', 'Othello']
		self.prev = 'kitchen'
		self.next = None
		self.chest_unlocked = False
		self.chest_opened = False
	def play(self, mode='repeat'):
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("You slowly walk down the stairs and into the secret basement. Again, you find a chest resting next to a large sofa. Dust is illuminated by the rays of sunshine flowing through the tiny window on your left. On your right is a tall bookcase with lots of books.")

class Polaris(Scene):
	def __init__(self):
		self.title = "polaris"
		self.key_found = False
		self.door_unlocked = False
		self.chest_unlocked = False
		self.chest_opened = False
		self.painting_moved = False
		self.objects = ['nothing']
		self.next = 'cottage'
		self.prev = None
		self.visits = 0
		self.repeat_messages = [
			'you revisit the empty, cold wasteland. you remember it being cold... it is still cold',
			'you jump from rock to rock, almost falling into the snow a few times',
			"you come back to your drop site, wondering if you can jump back through the portal... you can't"
		]
		self.monsters = {'example': Monster('easy')}
	def play(self, mode='repeat'):
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("you jump through the portal and arrive in a snowy landscape. the ground is frozen and the rocks nearby feel cold. you shiver in your thin pajamas. a sign nearby says that you are in Polaris. you walk a little further until you spot a house with smoke flowing out of the chimney.")

class Selva(Scene):
	def __init__(self):
		self.title = "selva"
		self.visits = 0
		self.repeat_messages = [
			'you walk backwards towards your drop site. you spot the same rusty sign as before...',
			'you are trying to go back to the drop site, but accidentally trip over a tree root. Ouch...',
			'you finally make it back to your drop site, jumping with joy. suddenly you hear a crackle nearby and you freeze. a small animal runs by, scaring you.'
		]
		self.objects = ['nothing']
		self.open_portal = False
		self.monsters = {'example': Monster('easy')}
		self.prev = None
		self.next = 'hut'
	def play(self, mode='repeat'):
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("you jump through the portal and land deep in the jungle. a rusty sign nearby tells you that you are in Selva. you walk forward, jumping over tree roots and ducking under branches. soon you can see a hut.")

class Cottage(Scene):
	def __init__(self):
		self.title = "cottage"
		self.chest_unlocked = False
		self.chest_opened = False
		self.objects = ['chest', 'sofa']
		self.next = 'shop'
		self.prev = 'tundra'
		self.visits = 0
		self.repeat_messages = [
			'you run back to the cottage, your fingers numb. you sit in front of the fire, slowly regaining feeling in your cold fingers. that was a close call!',
			'you enter the cottage again, but it seems different. weirdly, everything has been flipped as if you walked into a mirror... strange',
			'you walk into the cottage and lay down on the couch. as you slowly doze off, you are startled awake by a scream. unfortunately, you do not know where the scream came from and you quickly fall asleep'
		]
		self.monsters = {'example': Monster('easy')}
	def play(self, mode='repeat'):
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("you enter the cottage and instantly feel warmer. you find a small chest in the corner and a sofa. a fire is blazing in the fireplace, but there is no sign of another human.")

class Hut(Scene):
	def __init__(self):
		self.title = "hut"
		self.key_found = False
		self.chest_unlocked = False
		self.chest_opened = False
		self.objects = ['chest', 'key', 'tv']
		self.next = 'shop'
		self.prev = 'selva'
		self.visits = 0
		self.repeat_messages = [
			'you re-enter the hut in desperate need of escape from the intense heat',
			'you enter the hut again, hoping that you missed a bathroom of some sort to wipe off your sweat. sadly, you cannot find one...',
			'as you walk up to the hut, you trip. you bump your head on a small rock, causing some blood to trickle down the side of your face. Ouch...'
		]
		self.monsters = {'example': Monster('easy')}
	def play(self, mode='repeat'):
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("you enter the hut, temporarily shielded from the blazing sun. inside, you find another chest, a key, and a tv.")

class Shop(Scene):
	def __init__(self, landscape):
		self.title = "shop"
		self.objects = ['counter']
		if landscape == "tundra":
			self.next = 'cliff'
			self.prev = 'cottage'
		else:
			self.next = 'waterfall'
			self.prev = 'hut'
		self.visits = 0
		self.repeat_messages = [
			'you enter the shop again, hoping to buy more items',
			'you rush into the shop, throwing your gold at the vendor. you desperately needed more...',
			'you slowly walk into the shop, gently perusing the available items'
		]
		self.monsters = {'example': Monster('easy')}
		self.stock = {
			'apple': 5,
			'key': 5
		}
		self.prices = {
			'apple': 5,
			'key': 3
		}
	def play(self, mode='repeat'):
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("you enter the small shop, sort of disappointed in its lack of available items. you can currently buy either apples or keys.")

class Cliff(Scene):
	def __init__(self):
		self.title = "cliff"
		self.objects = ['tree']
		self.next = 'final'
		self.prev = 'shop'
		self.visits = 0
		self.repeat_messages = [
			"you desire the cliff's edge once again. you rush to the edge and pretend you are the king of the world. you gaze over the tundra, able to see the entire frontier",
			"you tentatively walk up to the edge, scared that you will fall. suddenly a strong wind pushes you and you slip. you barely hang on to the edge with your right hand, literally dangling 200 feet in the air. fortunately, you muster enough strength to pull yourself up. you vow never to go that close again",
			"you get to the cliff's edge and throw some rocks down. you enjoy the sound they make so you spend hours doing this..."
		]
		self.monsters = {'example': Monster('easy')}
	def play(self, mode='repeat'):
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("As you walk away from the shop, you notice a large mountain. you climb up it, quickly approaching a large cliff. you look over the edge and some rocks fall to the ground below. it's a loooooooooong fall")

class Waterfall(Scene):
	def __init__(self):
		self.title = "waterfall"
		self.chest_unlocked = False
		self.chest_opened = False
		self.objects = ['chest']
		self.next = 'final'
		self.prev = 'shop'
		self.visits = 0
		self.repeat_messages = [
			'in awe of the awesome waterfall, you come back to take a picture. sadly, you forgot that your phone is at home by your bedside table. no pictures today...',
			"already sweating, you decide to come back to the waterfall for a cold drink and a refreshing dip",
			"you come back to the waterfall, wanting to enjoy its presence for a little while. eventually you get bored and go for another swim"
		]
		self.monsters = {'example': Monster('easy')}
	def play(self, mode='repeat'):
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("after leaving the shop, you continue to journey through the jungle. eventually you come across a large waterfall. you take a couple sips of water and decide to go swimming. you finally get to cool down. soon you are standing behind the waterfall. there, you find another chest.")

class Final(Scene):
	def __init__(self, landscape):
		self.mode = landscape
		self.title = "boss"
		self.objects = ['nothing']
		self.next = None
		if landscape == 'tundra':
			self.prev = 'cliff'
			self.monsters = {'yeti': Monster('boss', 'abominable snowman')}
			self.repeat_messages = [
				'you come back to the area and the yeti still stands as tall as ever',
				"you decide that you can't run away from the fight...",
				"you hurriedly rush back to the yeti, still in awe it actually exists"
			]
			self.storyline = "in front of you stands a large beast. this yeti is twenty feet tall, white as snow, and weighs at least one thousand pounds."
		else:
			self.prev = 'waterfall'
			self.monsters = {'sasquatch': Monster('boss', 'sasquatch')}
			self.repeat_messages = [
				'you come back to the clearing, thinking that the sasquatch was only a mythical creature',
				"you hear a large roar from the sasquatch and hide behind some bushes. after a few minutes of silence, you come out of your hiding spot. you can see the sasquatch a few hundred yards away... scary",
				"after fleeing the area, you realize that you accidentally left a few apples behind. not wanting the beast to eat them, you rush back to grab them..."
			]
			self.storyline = "standing in a clearing is a large sasquatch, roughly ten feet tall. this beast is covered in brown fur and weighs about five hundred pounds."
		self.visits = 0
		
	def play(self, mode='repeat'):
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print(self.storyline)

class Death(Scene):
	def __init__(self):
		self.title = "death"
	def play(self):
		print(textwrap.dedent("""
		You died... DUN DUN DUNNNNNNNNNNNNNNN
		"""))

class Map:
	scenes = {
		'bedroom': Bedroom(), #choose to go on adventure (makes user and choose class and stuff)
		'kitchen': Kitchen(),
		'basement': Basement()
	}
	tundra_scenes = {
		'polaris': Polaris(),
		'cottage': Cottage(),
		'shop': Shop('tundra'),
		'cliff': Cliff(),
		'final': Final('tundra')
	}
	jungle_scenes = {
		'selva': Selva(),
		'hut': Hut(),
		'shop': Shop('jungle'),
		'waterfall': Waterfall(),
		'final': Final('jungle')
	}

	def __init__(self, first_scene='bedroom'):
		self.tundra = False
		self.jungle = False
		self.first_scene = Map.scenes.get(first_scene)

class Game:
	items = {
		'apple': 'atk +5',
		'key': 'usable to unlock doors and chests',
	}
	def __init__(self, mapobj):
		self.map = mapobj
		self.cur_scene = self.map.first_scene
		self.boss_defeated = False
	def start(self):
		while self.map.tundra != True or self.map.jungle != True:
			if self.cur_scene.visits == 0:
				self.cur_scene.play(mode='first')
				self.cur_scene.visits += 1
			else:
				self.cur_scene.play(mode='repeat')
			next_scene_name = Parser(self.cur_scene).next_scene
			self.cur_scene = Map.scenes.get(next_scene_name)
			if user.alive == False:
				break
			clear(1)
		if user.alive:
			if self.map.tundra:
				while self.boss_defeated == False:
					if self.cur_scene.visits == 0:
						self.cur_scene.play(mode='first')
						self.cur_scene.visits += 1
					else:
						self.cur_scene.play(mode='repeat')
					next_scene_name = Parser(self.cur_scene).next_scene
					self.cur_scene = Map.tundra_scenes.get(next_scene_name)
					if user.alive == False:
						break
					clear(1)
			elif self.map.jungle:
				while self.boss_defeated == False:
					if self.cur_scene.visits == 0:
						self.cur_scene.play(mode='first')
						self.cur_scene.visits += 1
					else:
						self.cur_scene.play(mode='repeat')
					next_scene_name = Parser(self.cur_scene).next_scene
					self.cur_scene = Map.jungle_scenes.get(next_scene_name)
					if user.alive == False:
						break
					clear(1)
		clear(1)
		if self.boss_defeated == True:
			clear()
			print("YOU WIN!!!!!!!!!!!!!!!")
		else:
			self.cur_scene = Death()
			self.cur_scene.play()
	def print_ui():
		clear(1)
		lvl_two = ['HP', 'ATK', 'Gold']
		selfvars = [user.name, user.lvl, user.xp]
		selfvars2 = [user.hp, user.atk, user.gold]

		#figuring out the dimensions
		max_char = 0
		string1 = "| {0} | Level: {1} ({2}/{3}) |".format(user.name, user.lvl, user.xp, User.xp_requirement[user.lvl])
		string2 = "| HP: {0}/{1} | ATK: {2} | Gold: {3} |".format(user.hp, user.maxhp, user.atk, user.gold)
		s1_sum = len(string1)
		s2_sum = len(string2)
		s1_spaces = s2_spaces = 0
		if s2_sum > s1_sum:
			if (s2_sum - s1_sum)%4 == 0:
				s1_spaces = (s2_sum-s1_sum)/4
			else:
				s1_spaces = 4-(s1_sum%4)
			s2_spaces = 4 - (s2_sum%4)
		elif s1_sum > s2_sum:
			if (s1_sum - s2_sum)%2 == 0:
				s2_spaces = (s1_sum-s2_sum)//2
			else:
				if (s1_sum - s2_sum) < 2:
					s2_spaces = 1
				else:
					s2_spaces = (s1_sum-s2_sum+1)//2
			s1_spaces = 4 - (s1_sum%4)
		#they should both try and pad for the same number (but the larger of the two)
		if s2_sum + s2_spaces > s1_sum + s1_spaces: 
			max_char = s2_sum + s2_spaces
			while s2_sum + s2_spaces != s1_sum + s1_spaces:
				s1_spaces += 1
		else:
			max_char = s1_sum + s1_spaces
			while s2_sum + s2_spaces != s1_sum + s1_spaces:
				s2_spaces += 1

		#printing the profile
		print('{0}'.format('-' * max_char))
		mid_space = 0
		end_space = 0
		while (s1_sum + mid_space + end_space) < (s1_sum + s1_spaces):
			if (s1_sum + mid_space + end_space) + 2 > (s1_sum + s1_spaces):
				end_space += 1
			else:
				mid_space += 2
		print("| {0} {4}| Level: {1} ({2}/{3}) {4}{5}|".format(user.name, user.lvl, user.xp, User.xp_requirement[user.lvl], mid_space//2*' ', end_space*' '))
		print('|{0}|'.format('-'*(max_char-2)))
		mid_space = 0
		end_space = 0
		while (s2_sum + mid_space + end_space) < (s2_sum + s2_spaces):
			if (s2_sum + mid_space + end_space) + 3 > (s2_sum + s2_spaces):
				end_space += 1
			else:
				mid_space += 3
		print("| HP: {0}/{1} {4}| ATK: {2} {4}| Gold: {3} {4}{5}|".format(user.hp, user.maxhp, user.atk, user.gold, mid_space//3*' ', end_space*' '))
		print('{0}'.format('-' * max_char))
		cont()
	def view_inventory():
		clear(1)
		inv = user.inventory
		title("{}'s Inventory:\n".format(user.name))
		print_items = []
		for key in inv:
			print("{}: {}".format(key, inv[key]))
		user.inventory = inv

		cont()

class Parser:
	def __init__(self, cur_scene):
		self.scene = cur_scene
		self.next_scene = None
		self.handle_action()
	def handle_action(self):
		while self.next_scene == None:
			action = input("[command]> ")
			if action != "":
				check_action = action.split()
				obj = check_action[-1]
				if obj != 'nothing':
					if 'a' in check_action or 'attack' in check_action:
						if obj in self.scene.monsters.keys():
							Battle(user, self.scene.monsters.get(obj))
							if user.alive and self.scene.title == 'final':
								new_game.boss_defeated = True
						else:
							print("you cannot attack this monster...")
					elif 'b' in check_action or 'backpack' in check_action:
						if obj == 'backpack' or obj == 'b':
							Game.view_inventory()
						else:
							if obj in user.inventory.keys():
								print("{}: {}".format(obj, user.inventory[obj]))
							else:
								print("you cannot view this item...")
					elif 'c' in check_action or 'consume' in check_action:
						if obj in ['apple', 'potion', 'water']:
							if user.inventory[obj] >= 1:
								user.inventory[obj] -= 1
								if obj == 'apple':
									user.atk += 10
									user.hp += 15
									print("your atk has been raised by 10 points and your hp has been raised by 15 points!")
								elif obj == 'potion':
									miss_hp_50 = (user.maxhp - user.hp)//2
									print("your hp has been restored by {} points!".format(miss_hp_50))
									user.hp += miss_hp_50
								elif obj == 'water':
									user.hp += 5
									print("your hp has been restored by 5 points!")
							else:
								print("you do not have a(n) {}".format(obj))
						else:
							print("you cannot consume that...")
					elif 'd' in check_action or 'discard' in check_action:
						if user.inventory[obj] >= 1:
							print("you discarded {}...".format(obj))
							user.inventory[obj] -= 1
						else:
							print("you cannot discard this item...")
					elif 'e' in check_action or 'erase' in check_action:
						clear()
					elif 'g' in check_action or 'go' in check_action:
						if obj in Map.scenes.keys():
							if obj == self.scene.next or obj == self.scene.prev:
								self.next_scene = obj
							else:
								print("you cannot go here...")
						else:
							print("you cannot go here...")
					elif 'h' in check_action or 'help' in check_action:
						print(help_menu)
					elif 'i' in check_action or 'interact' in check_action:
						if obj in self.scene.objects:
							if obj == 'bed':
								print("you get back into bed, hoping for five more minutes of sleep. You succeed and fall back asleep.")
							elif obj == 'bookcase':
								if self.scene.open_portal:
									print("you move the bookcase to the side, revealing a portal. a note nearby says that the portal is only one-way, meaning once you go through, you can never go back.")
									print("Are you sure you want to go through the portal?")
									n = input("[yes/no]> ")
									while n != 'yes' and n != 'no':
										print("enter 'yes' or 'no'")
										print("Are you sure you want to go through the portal?")
										n = input('[yes/no]> ')
									if n == 'yes':
										self.next_scene = path_picker()
									else:
										print("you back away from the portal, scared of its power.")
								else:
									print("Do you want to read a book?")
									n = input("[yes/no]> ").lower()
									while n != 'yes' and n != 'no':
										print("Do you want to read a book?")
										n = input("[yes/no]> ").lower()
									if n == 'yes':
										book_picker(self.scene)
									else:
										print("you walk away from the bookshelf... not wanting to read a book")
							elif obj == 'chest':
								responses = [
									"you kick the chest... it doesn't do anything",
									"you try to move the chest, but it appears to be bolted to the floor",
									"you sit on the chest. your butt is kinda uncomfy so you stand yet again"
								]
								print(random.choice(responses))
							elif obj == 'counter':
								print("what do you want to buy?")
								n = input("[apple/key]> ").lower()
								while n != 'apple' and n != 'key':
									print("what do you want to buy?")
									n = input("[apple/key]> ").lower()
								for item in self.scene.stock:
									print("{} in stock: {}".format(item, self.scene.stock[item]))
								for item in self.scene.prices:
									print("{} price: {} gold".format(item, self.scene.prices[item]))
								if n == 'apple':
									print("how many apples do you want to buy?")
									n = int(input("[int]> "))
									while n < 0 or n > self.scene.stock['apple'] or (n*self.scene.prices['apple']) > user.gold:
										print("you cannot buy that many...")
										print('how many do you want to buy?')
										n = int(input("[int]> "))
									user.inventory['apple'] += n
									self.scene.stock['apple'] -= n
									user.gold -= (n * self.scene.prices['apple'])
								else:
									print("how many keys do you want to buy?")
									n = int(input("[int]> "))
									while n < 0 or n > self.scene.stock['key'] or (n*self.scene.prices['key']) > user.gold:
										print("you cannot buy that many...")
										print('how many do you want to buy?')
										n = int(input("[int]> "))
									user.inventory['key'] += n
									self.scene.stock['key'] -= n
									user.gold -= (n * self.scene.prices['key'])
							elif obj == 'door':
								if self.scene.door_unlocked:
									print("you opened the door!")
									if self.scene.title == 'bedroom':
											print("you push the door open and look into the kitchen. you walk through the doorway.")
											self.next_scene = 'kitchen'
									if self.scene.title == 'kitchen':
										print("you push the door open, staring back at your bedroom. you walk through the doorway.")
										self.next_scene = 'bedroom'
								else:
									print("the door is locked...")
							elif obj == 'key':
								if self.scene.key_found:
									print("you took the key already...")
								else:
									self.scene.key_found = True
									print("you picked up the key.")
									user.inventory['key'] += 1
							elif obj == 'painting':
								if self.scene.title == 'bedroom':
									if self.scene.painting_moved:
										print("you look at your smashed painting, wishing that you hadn't done that. too bad, you don't have the power to travel back in time...yet")
									else:
										self.scene.painting_moved = True
										print("you grab the painting of you and your mother off the wall and slam it to the ground. the wood frame cracks, warping the painting. behind the painting, there is nothing but a wall and the nail it was hanging on. sad, you just broke your painting...")
								if self.scene.title == 'kitchen':
									if self.scene.painting_moved:
										print("")
									else:
										self.scene.painting_moved = True
										print("you notice that the painting is slightly askew. being the perfectionist that you are, you try to correct it. suddenly, a key falls out from behind it, dropping to the floor. you pick up the key.")
										user.inventory['key'] += 1
							elif obj == 'refrigerator':
								if self.scene.title == 'kitchen':
									if self.scene.refrigerator_unlocked == False:
										print("you open the refrigerator, but only find a moldy apple and some rotten cheese...")
									else:
										print("you push the refrigerator to the side, revealing the staircase behind it.")
										self.next_scene = 'basement'
							elif obj == 'sofa':
								if self.scene.title == 'basement':
									print("you sit down on the sofa, resting for a little bit. curious, you search the couch cushions and find two spare keys. YAY what a great find!")
									user.inventory['key'] += 2
								if self.scene.title == 'cottage':
									print("you rest on the sofa, catching up on some sleep...")
							elif obj == 'tree':
								if self.scene.title == 'cliff':
									print('luckily, this tree happens to be an apple tree! you pick the fruit and gain 8 apples. YAY')
									user.inventory['apple'] += 8
							elif obj == 'tv':
								if self.scene.title == 'hut':
									print("you want to watch tv but can't find the remote. oh well...")
							elif obj == 'window':
								responses = [
									"you tap on the glass and it cracks. you decide not to tap the glass anymore",
									"you push on the window but it holds still. you have a very sturdy window",
									"you look out the window at the nearby tree, wondering what it would be like to be a bird"
								]
								print(random.choice(responses))
							else:
								print("you cannot interact with that...")
						else:
							print("you cannot interact with that...")
					elif 'l' in check_action or 'look' in check_action:
						if obj in Game.items:
							print(Game.items[obj])
						elif obj in self.scene.objects:
							if obj == 'bookcase':
								print('bookcase: a place to store books. books such as....')
								for book in self.scene.books:
									print("[-] {}".format(book))
							elif obj == 'chest':
								print('chest: a body part OR a box that sometimes holds treasure')
							elif obj == 'door':
								print('door: a block of material that separates two rooms')
							elif obj == 'painting':
								print('painting: something pricey, something artistic, something decorative')
							elif obj == 'refrigerator':
								print('refrigerator: a cool place to store food or anything else you desire')
							elif obj == 'sofa':
								print('sofa: a place to lay down and stay down for the entire day')
							elif obj == 'window':
								print('window: a place to look longingly at the outdoors')
						else:
							print("you cannot look at this...")
					elif 'm' in check_action or 'map' in check_action:
						unlocked_scenes = []
						for scene in new_map.scenes:
							scene = new_map.scenes.get(scene)
							if scene.visits >= 1:
								unlocked_scenes.append(scene.title)
							else:
								unlocked_scenes.append("?")
						if new_map.tundra:
							for scene in new_map.tundra_scenes:
								scene = new_map.tundra_scenes.get(scene)
								if scene.visits >= 1:
									unlocked_scenes.append(scene.title)
								else:
									unlocked_scenes.append("?")
						if new_map.jungle:
							for scene in new_map.jungle_scenes:
								scene = new_map.jungle_scenes.get(scene)
								if scene.visits >= 1:
									unlocked_scenes.append(scene.title)
								else:
									unlocked_scenes.append("?")
						for title in unlocked_scenes:
							print("{} => ".format(title), end="")
						print('?', end="")
						print('')
					elif 'o' in check_action or 'open' in check_action:
						if obj in self.scene.objects:
							if obj == 'door':
								if self.scene.door_unlocked == False:
									print("the door is locked...")
								else:
									if self.scene.title == 'bedroom':
										print("you push the door open and look into the kitchen. you walk through the doorway.")
										self.next_scene = 'kitchen'
									if self.scene.title == 'kitchen':
										print("you push the door open, staring back at your bedroom. you walk through the doorway.")
										self.next_scene = 'bedroom'
							elif obj == 'chest':
								if self.scene.chest_unlocked == False:
									print("the chest is locked...")
								else:
									if self.scene.chest_opened:
										print("you open the chest and realize you have already taken the contents...")
									else:
										if self.scene.title == 'bedroom':
											user.inventory['key'] += 1
											user.gold += 15
											print("wow... you found 15 gold and another key")
										if self.scene.title == 'kitchen':
											user.inventory['key'] += 1
											user.inventory['apple'] += 2
											print('wowza... you found 2 apples and a key')
										if self.scene.title == 'basement':
											user.inventory['key'] += 1
											print('huzzah... another key!')
										if self.scene.title == 'cottage':
											user.inventory['apple'] += 3
											user.inventory['key'] += 2
											print("WOO... you found treasure!")
										if self.scene.title == 'hut':
											user.inventory['apple'] += 3
											user.inventory['key'] += 2
											print("WOO... you got lots of treasure!")
										if self.scene.title == 'waterfall':
											user.inventory['apple'] += 8
											print("YAYYYYY apples...")
										self.scene.chest_opened = True
							elif obj == 'refrigerator':
								if self.scene.title == 'kitchen':
									print("you open the refrigerator, but only find a moldy apple and some rotten cheese...")
							elif obj == 'window':
								if self.scene.title == 'bedroom':
									print("you open the window and jump out. unfortunately, you forgot that you were on the third story and fell down into thorny bushes.")
									user.alive = False
									self.next_scene = 'death'
								if self.scene.title == 'kitchen':
									print("you opened the window and a small bird flew inside. it sung a little song. a few minutes later, it flew out again. then you closed the window.")
						else:
							print('you cannot open that...')
					elif 'p' in check_action or 'profile' in check_action:
						Game.print_ui()
					elif 's' in check_action or 'scan' in check_action:
						print("\nInteractable Objects:")
						for item in self.scene.objects:
							print("[-] {}".format(item))
					elif 'u' in check_action or 'unlock' in check_action:
						if obj in self.scene.objects:
							if user.inventory['key'] == 0:
								print("you do not have a key...")
							else:
								if obj == 'door':
									if self.scene.door_unlocked == False:
										self.scene.door_unlocked = True
										user.inventory['key'] -= 1
										print('you unlocked the door.')
									else:
										print("you already unlocked the door... open it instead")
								elif obj == 'chest':
									if self.scene.chest_unlocked == False:
										self.scene.chest_unlocked = True
										user.inventory['key'] -= 1
										print('you unlocked the chest. open it!')
									else:
										print("the chest is already unlocked... open it instead.")
								elif obj == 'refrigerator':
									if self.scene.refrigerator_unlocked == False:
										self.scene.refrigerator_unlocked = True
										user.inventory['key'] -= 1
										print("you insert your key into a small keyhole on the handle. you turn the key and hear a lock click open. what could be behind the refrigerator?")
									else:
										print("you already unlocked the refrigerator... open it instead")
						else:
							print('you cannot unlock that...')
		cont()

#finally... the actual game :)
intro()
user = User()
new_map = Map()
new_game = Game(new_map)
new_game.start()