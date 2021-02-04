import random, time, os, math, textwrap, sys

'''
WARNING: I'm not sure if anyone will read this, but there is a bug and I have no idea how to fix it :/
Once you defeat the final boss, the game won't end. You can do whatever you want (there isn't much), but
I included a quit function in the game. Type 'q' or 'quit' to end the game. Yay.........................

Also, if you use a different program to run this code (I used Visual Studio Code),
the formatting might be messed up... Oh well.
'''

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
	backpack (b): see inside your inventory
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
	quit (q): quits the game
	scan (s): scans the room for a list of interactable objects
	unlock (u) [item]: unlock something by using up one key
"""
shop_stock = """
|-----------------------|
|_______| stock | price |
| apple |     5 |     5 |
| key   |     5 |     3 |
|-----------------------|
"""

#general, helpful functions
def title(title):
	print('{}: \n'.format(title))
def clear(t=0):
	time.sleep(t)
	os.system('clear')
def cont():
	input("\n press [enter] to continue ")


#character classes
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
			self.reward = [1, 25] #[gold,xp]
		elif difficulty == 'medium':
			self.hp = random.randint(30,150)
			self.atk = random.randint(5,15)
			self.reward = [5, 50] #[gold,xp]
		elif difficulty == 'hard':
			self.hp = random.randint(60,300)
			self.atk = random.randint(10,30)
			self.reward = [10, 100] #[gold,xp]
		else: #boss levels
			self.hp = random.randint(150,300)
			self.atk = random.randint(25,50)
			self.reward = [50, 1000] #[gold,xp]


class User:
	classes = ['peasant', 'wizard', 'warrior', 'tank', 'gambler']
	hp = {'peasant': 100, 'wizard': 80, 'warrior': 70, 'tank': 150, 'gambler': random.randint(50, 170), 'god': 10000000000}
	atk = {'peasant': 50, 'wizard': 80, 'warrior': 100, 'tank': 30, 'gambler': random.randint(10, 120), 'god': 10000000000}
	xp_requirement = [100, 100, 200, 250, 300, 500, 500, 750, 1000, 2500, 5000, 7500, 7500, 8000, 1000] #total of 15 levels at the moment

	def __init__(self):
		self.inventory = {'apple': 0, 'key': 0}
		self.lvl = 1
		self.xp = 0
		self.gold = 0
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
			print("\nEnter the name of a class!")
			user_class = input("[class name]> ")
		self.hp = User.hp.get(user_class)
		self.maxhp = self.hp
		self.atk = User.atk.get(user_class)
		print("\nYour hp is {0} and your atk is {1}.".format(self.hp, self.atk))
		clear(5)
	
	def level_up(self): #run after every xp-gaining activity (battles, 'quests', xp_potions, [other])
		while self.xp >= User.xp_requirement[self.lvl]:
			if self.lvl == 15:
				print("You've reached the max level of 15!")
				break
			self.xp -= User.xp_requirement[self.lvl]
			self.lvl += 1
			self.atk = int(self.atk * 1.25)
			self.hp = int(self.hp * 1.5)
			self.maxhp = self.hp
			print("You leveled up! Your level is now {}".format(self.lvl))
			time.sleep(1)
	
	def get_reward(self, rewards):
		self.gold += rewards[0]
		self.xp += rewards[1]
		print("\nYAY! You were rewarded with {} gold and {} xp!".format(rewards[0], rewards[1]))
		self.level_up()
	# def get_quest(self):
	def print_ui(self):
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
	
	def view_inventory(self):
		title("{}'s Inventory".format(user.name))
		for key in user.inventory:
			print("""
	{}: {}""".format(key, user.inventory[key]))


class Battle:
	def __init__(self, user, monster):
		self.winner = None
		print("Are you sure you want to battle?")
		n = input("[yes/no]> ")
		while n != 'yes' and n != 'no':
			print("Enter 'yes' or 'no'...")
			print("Are you sure you want to battle?")
			n = input("[yes/no]> ")
		if n == 'yes':
			self.start(user, monster)
		else:
			print("You fled from the monster, too scared to fight.")
	
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
			time.sleep(2)
		if self.winner == user:
			print("You win!")
			new_game.boss_defeated = True
			user.get_reward(monster.reward)
			cont()
		else:
			user.alive = False


#scene classes... yay
class Scene: #YAY GOTHONS -- teaching me how to use inheritance better :)
	def __init__(self):
		self.title = "example"
		self.prev_scene = 'death'
		self.next_scene = 'death'
		self.travel = False
		self.visits = 0
		self.repeat_messages = [
			'You entered the scene yet again. Nothing has changed.',
			'yYou walk into the scene, discovering that everything has been destroyed. Oh well...'
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
		self.prev = 'example'
		self.visits = 0
		self.repeat_messages = [
			'You walk into the bedroom and see that everything has been cleaned. Your bed is made, the floor has no clothes, and your windows are no longer dusty. You wonder who could have done this...',
			'You enter your bedroom and everything is the same. Quite boring.',
			'The bedroom looks the same, except you understand that everything has been replaced with an exact replica.'
		]
		self.monsters = {'example': Monster('easy')}
	def play(self, mode='repeat'):
		title("Bedroom")
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("You slowly open your eyes, squinting at the bright light shining through your window. You look at your watch, reading that it's 8:07 AM. You get out of bed and get dressed. In your room, there is a chest, a painting, and a window. There is also a key sitting on your bedside table. You walk over to your bedroom door, only to discover that it is locked.")


class Kitchen(Scene):
	def __init__(self):
		self.title = "kitchen"
		self.travel = False
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
		title("Kitchen")
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("You walk into the kitchen, almost slipping on the slick tile floor. You stand next to the refrigerator, admiring the painting hanging next to the window. Beside the bedroom door, there is another chest.")


class Basement(Scene):
	def __init__(self):
		self.title = "basement"
		self.travel = False
		self.visits = 0
		self.repeat_messages = [
			'You walk back down into the basement, still in awe it was hidden from you for your entire life.',
			'You start walking down the stairs but accidentally stumble and fall, landing hard on the concrete floor. Ouch.',
			'You rush down the stairs in a hurry. After a few seconds, you stop. Why were you in such a hurry?'
		]
		self.objects = ['chest', 'window', 'sofa', 'bookcase', 'staircase']
		self.open_portal = False
		self.monsters = {'example': Monster('easy')}
		self.prev = 'kitchen'
		self.next = 'example'
		self.chest_unlocked = False
		self.chest_opened = False
	def play(self, mode='repeat'):
		title("Basement")
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("You slowly walk down the stairs and into the secret basement. Again, you find a chest resting next to a large sofa. Dust is illuminated by the rays of sunshine flowing through the tiny window on your left. On your right is a tall bookcase with lots of books.")


class Polaris(Scene):
	def __init__(self):
		self.title = "polaris"
		self.travel = False
		self.key_found = False
		self.door_unlocked = False
		self.chest_unlocked = False
		self.chest_opened = False
		self.painting_moved = False
		self.objects = ['path']
		self.next = 'cottage'
		self.prev = 'example'
		self.visits = 0
		self.repeat_messages = [
			'You revisit the empty, cold wasteland. You remember it being cold... it is still cold.',
			'You jump from rock to rock, almost falling into the snow a few times.',
			"You come back to your drop site, wondering if you can jump back through the portal... you can't..."
		]
		self.monsters = {'example': Monster('easy')}
	def play(self, mode='repeat'):
		title("Polaris")
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("You jump through the portal and arrive in a snowy landscape. The ground is frozen and the rocks nearby feel cold. You shiver in your thin pajamas. A sign nearby says that you are in Polaris. You walk a little further until you spot a house with smoke flowing out of the chimney. Leading up to it is a dirt path.")


class Selva(Scene):
	def __init__(self):
		self.title = "selva"
		self.travel = False
		self.visits = 0
		self.repeat_messages = [
			'You walk backwards towards your drop site. You spot the same rusty sign as before...',
			'You are trying to go back to the drop site, but accidentally trip over a tree root. Ouch...',
			'You finally make it back to your drop site, jumping with joy. Suddenly you hear a crackle nearby and you freeze. A small animal runs by, scaring you.'
		]
		self.objects = ['trail']
		self.open_portal = False
		self.monsters = {'example': Monster('easy')}
		self.prev = 'example'
		self.next = 'hut'
	def play(self, mode='repeat'):
		title("Selva")
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("You jump through the portal and land deep in the jungle. A rusty sign nearby tells you that you are in Selva. You walk forward, jumping over tree roots and ducking under branches. Soon you can see a hut and a trail nearby.")


class Cottage(Scene):
	def __init__(self):
		self.title = "cottage"
		self.travel = False
		self.chest_unlocked = False
		self.chest_opened = False
		self.door_unlocked = False
		self.objects = ['chest', 'sofa', 'door', 'path']
		self.next = 'shop'
		self.prev = 'tundra'
		self.visits = 0
		self.repeat_messages = [
			'You run back to the cottage, your fingers numb. You sit in front of the fire, slowly regaining feeling in your cold fingers. That was a close call!',
			'You enter the cottage again, but it seems different. Weirdly, everything has been flipped as if you walked into a mirror... strange',
			'You walk into the cottage and lay down on the couch. As you slowly doze off, you are startled awake by a scream. Unfortunately, you do not know where the scream came from and you quickly fall asleep'
		]
		self.monsters = {'example': Monster('easy')}
	def play(self, mode='repeat'):
		title("Cottage")
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("You enter the cottage and instantly feel warmer. You find a small chest in the corner and a sofa. A fire is blazing in the fireplace, but there is no sign of another human. Towards the back of the room is another door.")


class Hut(Scene):
	def __init__(self):
		self.title = "hut"
		self.travel = False
		self.key_found = False
		self.chest_unlocked = False
		self.chest_opened = False
		self.door_unlocked = False
		self.objects = ['chest', 'key', 'tv', 'door', 'trail']
		self.next = 'shop'
		self.prev = 'selva'
		self.visits = 0
		self.repeat_messages = [
			'You re-enter the hut in desperate need of escape from the intense heat',
			'You enter the hut again, hoping that you missed a bathroom of some sort to wipe off your sweat. Sadly, you cannot find one...',
			'As you walk up to the hut, you trip. You bump your head on a small rock, causing some blood to trickle down the side of your face. Ouch...'
		]
		self.monsters = {'example': Monster('easy')}
	def play(self, mode='repeat'):
		title("Hut")
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("You enter the hut, temporarily shielded from the blazing sun. Inside, you find another chest, a key, and a tv. There is another room to your right, connected by a door.")


class Shop(Scene):
	def __init__(self, landscape):
		self.title = "shop"
		self.travel = False
		self.objects = ['counter', 'door', 'trail']
		if landscape == "tundra":
			self.next = 'cliff'
			self.prev = 'cottage'
		else:
			self.next = 'waterfall'
			self.prev = 'hut'
		self.visits = 0
		self.door_unlocked = True
		self.repeat_messages = [
			'You enter the shop again, hoping to buy more items',
			'You rush into the shop, throwing your gold at the vendor. You desperately needed more...',
			'You slowly walk into the shop, gently perusing the available items'
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
		title("Shop")
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("You enter the small shop, sort of disappointed in its lack of available items. You can currently buy either apples or keys.")


class Cliff(Scene):
	def __init__(self):
		self.title = "cliff"
		self.travel = False
		self.objects = ['tree', 'trail', 'path']
		self.next = 'boss'
		self.prev = 'shop'
		self.visits = 0
		self.repeat_messages = [
			"You desire the cliff's edge once again. You rush to the edge and pretend you are the king of the world. You gaze over the tundra, able to see the entire frontier.",
			"You tentatively walk up to the edge, scared that you will fall. Suddenly a strong wind pushes you and you slip. You barely hang on to the edge with your right hand, literally dangling 200 feet in the air. Fortunately, you muster enough strength to pull yourself up. You vow never to go that close again.",
			"You get to the cliff's edge and throw some rocks down. You enjoy the sound they make so you spend hours doing this..."
		]
		self.monsters = {'example': Monster('easy')}
		self.tree_picked = False
	def play(self, mode='repeat'):
		title("Cliff")
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("As you walk away from the shop, you notice a large mountain. You climb up it, quickly approaching a large cliff. For a few seconds, you rest beneath a nearby tree. Eventually, you get up and look over the edge, kicking some rocks. It's a loooooooooong fall!")


class Waterfall(Scene):
	def __init__(self):
		self.title = "waterfall"
		self.travel = False
		self.chest_unlocked = False
		self.chest_opened = False
		self.objects = ['chest', 'trail', 'path']
		self.next = 'boss'
		self.prev = 'shop'
		self.visits = 0
		self.repeat_messages = [
			'In awe of the awesome waterfall, you come back to take a picture. Sadly, you forgot that your phone is at home by your bedside table. no pictures today...',
			"Already sweating, you decide to come back to the waterfall for a cold drink and a refreshing dip.",
			"You come back to the waterfall, wanting to enjoy its presence for a little while. Eventually you get bored and go for another swim."
		]
		self.monsters = {'example': Monster('easy')}
	def play(self, mode='repeat'):
		title("Waterfall")
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print("You follow the sound of the waterfall until you find it. You take a couple sips of water and decide to go swimming. You finally get to cool down. Soon you are standing behind the waterfall. There, you find another chest.")


class Final(Scene):
	def __init__(self, landscape):
		self.mode = landscape
		self.title = "boss"
		self.travel = False
		self.objects = ['path']
		self.next = 'example'
		if landscape == 'tundra':
			self.prev = 'cliff'
			self.monsters = {'yeti': Monster('boss', 'Abominable Snowman')}
			self.repeat_messages = [
				'You come back to the area and the yeti still stands as tall as ever.',
				"You decide that you can't run away from the fight...",
				"You hurriedly rush back to the yeti, still in awe it actually exists."
			]
			self.storyline = "In front of you stands a large beast. This yeti is twenty feet tall, white as snow, and weighs at least one thousand pounds."
		else:
			self.prev = 'waterfall'
			self.monsters = {'sasquatch': Monster('boss', 'sasquatch')}
			self.repeat_messages = [
				'You come back to the clearing, thinking that the sasquatch was only a mythical creature.',
				"You hear a large roar from the sasquatch and hide behind some bushes. After a few minutes of silence, you come out of your hiding spot. You can see the sasquatch a few hundred yards away... Scary!",
				"After fleeing the area, you realized that you accidentally left a few apples behind. Not wanting the beast to eat them, you rush back to grab them..."
			]
			self.storyline = "Standing in a clearing is a large sasquatch, roughly ten feet tall. This beast is covered in brown fur and weighs about five hundred pounds."
		self.visits = 0
		
	def play(self, mode='repeat'):
		title("Final")
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print(self.storyline)


class Death(Scene):
	def __init__(self):
		self.title = "death"
		self.travel = False
	def play(self):
		print(textwrap.dedent("""
		You died... DUN DUN DUNNNNNNNNNNNNNNN
		"""))


#map object
class Map:
	scenes = {
		'example': Scene(),
		'bedroom': Bedroom(), #choose to go on adventure (makes user and choose class and stuff)
		'kitchen': Kitchen(),
		'basement': Basement()
	}
	tundra_scenes = {
		'polaris': Polaris(),
		'cottage': Cottage(),
		'shop': Shop('tundra'),
		'cliff': Cliff(),
		'boss': Final('tundra')
	}
	jungle_scenes = {
		'selva': Selva(),
		'hut': Hut(),
		'shop': Shop('jungle'),
		'waterfall': Waterfall(),
		'boss': Final('jungle')
	}

	def __init__(self, first_scene='bedroom'):
		self.tundra = False
		self.jungle = False
		self.first_scene = Map.scenes.get(first_scene)


#game object
class Game:
	items = {
		'apple': 'atk +10, hp +15',
		'key': 'usable to unlock doors or chests',
	}
	def __init__(self):
		self.map = Map()
		self.cur_scene = self.map.first_scene
		self.boss_defeated = False
		clear()
		self.intro()

	def intro(self):
		clear()
		print("Welcome to The Wanderer!\n")
		time.sleep(2)
		print("""
	Hint: if you need help, type 'h' or 'help'""")
		clear(5)

	def start(self):
		global user
		user = User()

		#i needed separate game loops for the main realm and either the tundra or jungle realm...
		while self.map.tundra != True or self.map.jungle != True:
			if self.cur_scene.visits == 0:
				self.cur_scene.travel = True
				self.cur_scene.play(mode='first')
				self.cur_scene.visits += 1
			else:
				self.cur_scene.play(mode='repeat')
			next_scene_name = Parser(self.cur_scene).next_scene
			self.cur_scene = self.map.scenes.get(next_scene_name)
			clear(1)
			if user.alive == False:
				break
			if self.map.tundra == True or self.map.jungle == True:
				break
		if user.alive:
			if self.map.tundra:
				self.cur_scene = self.map.tundra_scenes.get('polaris')
				while not self.boss_defeated:
					if self.cur_scene.visits == 0:
						self.cur_scene.play(mode='first')
						self.cur_scene.visits += 1
					else:
						self.cur_scene.play(mode='repeat')
					next_scene_name = Parser(self.cur_scene).next_scene
					self.cur_scene = self.map.tundra_scenes.get(next_scene_name)
					clear(1)
					if user.alive == False:
						break
					if self.boss_defeated:
						break
			elif self.map.jungle:
				self.cur_scene = self.map.jungle_scenes.get('selva')
				while not self.boss_defeated:
					if self.cur_scene.visits == 0:
						self.cur_scene.play(mode='first')
						self.cur_scene.visits += 1
					else:
						self.cur_scene.play(mode='repeat')
					next_scene_name = Parser(self.cur_scene).next_scene
					self.cur_scene = self.map.jungle_scenes.get(next_scene_name)
					clear(1)
					if user.alive == False:
						break
					if self.boss_defeated:
						break
		clear(1)
		if self.boss_defeated == True:
			clear()
			print("YOU WIN!!!!!!!!!!!!!!!")
		else:
			self.cur_scene = Death()
			self.cur_scene.play()

	def book_picker(self, scene):
		book_responses = [
			'The book was exciting... YAY!',
			'You fell asleep while reading the book... Oh well...',
			'You slowly made your way through the book. You were unhappy, but still wanted to know what happened at the end...'
		]
		book_titles = ['Harry Potter and the Prisoner of Azkaban (HPPA)', 'Moby Dick (MD)', 'The Lion, the Witch, and the Wardrobe (LWW)', 'Winnie the Pooh (WP)', 'Romeo and Juliet (RJ)']
		books = ['harry potter and the prisoner of azkaban', 'hppa', 'moby dick', 'md', 'the lion, the witch, and the wardrobe', 'lww', 'winnie the pooh', 'wp', 'romeo and juliet', 'rj']
		print("\nBooks:")
		for book in book_titles:
			print("[-] {}".format(book))
		book = input("\n[book title]> ").lower()
		while book not in books:
			print("Enter a book title")
			book = input("\n[book title]> ")
		if book == 'the lion, the witch, and the wardrobe' or 'lww':
			scene.open_portal = True
			scene.objects.append('portal')
			print("\nYou try to take out the book, but it holds still. You try again, this time pulling from the top of the book. To your surprise, the book moves like a lever and you hear a click. You slide the bookcase to the side, revealing a portal.")
		else:
			print(random.choice(book_responses))

	def path_picker(self):
		print("\nWould you like to go to the jungle or the tundra?")
		n = input("[jungle/tundra]> ").lower()
		while n != 'jungle' and n != 'tundra':
			print("Enter 'jungle' or 'tundra'...")
			print("\nWould you like to go to the jungle or the tundra?")
			n = input("[jungle/tundra]> ").lower()
		if n == 'jungle':
			new_game.map.jungle = True
			return 'selva'
		else:
			new_game.map.tundra = True
			return 'polaris'


#oof... the large parser (which may not be formatted the way dr. b wanted...)
class Parser:
	def __init__(self, cur_scene):
		self.scene = cur_scene
		self.next_scene = None
		self.handle_action()
	def handle_action(self):
		while self.next_scene == None:
			action = input("\n[command]> ")
			if action != "":
				check_action = action.split()
				obj = check_action[-1]
				if 'a' in check_action or 'attack' in check_action:
					if obj in self.scene.monsters.keys():
						Battle(user, self.scene.monsters.get(obj))
					else:
						print("you cannot attack this monster...")
				elif 'b' in check_action or 'backpack' in check_action:
					if obj == 'backpack' or obj == 'b':
						user.view_inventory()
				elif 'c' in check_action or 'consume' in check_action:
					if obj in user.inventory.keys():
						if obj == 'apple':
							if user.inventory['apple'] >= 1:
								for _ in range(user.inventory['apple']):
									user.inventory['apple'] -= 1
									user.atk += 10
									user.hp += 15
									user.maxhp += 15
									print("Your atk has been raised by 10 points and your hp has been raised by 15 points!")
									time.sleep(0.25)
								print("Your atk is {} and your hp is {}!".format(user.atk, user.hp))
							else:
								print("you do not have an {}...".format(obj))
						else:
							print("you cannot consume that...")
					else:
						print("you cannot consume that...")
				elif 'd' in check_action or 'discard' in check_action:
					if obj in user.inventory.keys():
						if user.inventory[obj] >= 1:
							print("you discarded a(n) {}...".format(obj))
							user.inventory[obj] -= 1
						else:
							print("you cannot discard this item...")
					else:
						print('you cannot discard this item...')
				elif 'e' in check_action or 'erase' in check_action:
					clear()
				elif 'g' in check_action or 'go' in check_action:
					if obj in Map.scenes.keys():
						new_scene = new_game.map.scenes.get(obj)
						if obj == self.scene.next and new_scene.travel:
							self.next_scene = self.scene.next
						elif obj == self.scene.prev and new_scene.travel:
							self.next_scene = self.scene.prev
						else:
							print("you cannot go here...")
					elif obj in Map.tundra_scenes.keys():
						new_scene = new_game.map.tundra_scenes.get(obj)
						if obj == self.scene.next and new_scene.travel:
							self.next_scene = self.scene.next
						elif obj == self.scene.prev and new_scene.travel:
							self.next_scene = self.scene.prev
						else:
							print("you cannot go here...")
					elif obj in Map.jungle_scenes.keys():
						new_scene = new_game.map.jungle_scenes.get(obj)
						if obj == self.scene.next and new_scene.travel:
							self.next_scene = self.scene.next
						elif obj == self.scene.prev and new_scene.travel:
							self.next_scene = self.scene.prev
						else:
							print("you cannot go here...")
					else:
						print("you cannot go here...")
				elif 'h' in check_action or 'help' in check_action:
					print(help_menu)
				elif 'i' in check_action or 'interact' in check_action:
					if obj in self.scene.objects:
						if obj == 'bed':
							print("You get back into bed, hoping for five more minutes of sleep. You succeed and fall back asleep. Suddenly, a bird taps on your window and jolts you awake. Oops!")
						elif obj == 'bookcase':
							print("\nDo you want to read a book?")
							n = input("[yes/no]> ").lower()
							while n != 'yes' and n != 'no':
								print("\nDo you want to read a book?")
								n = input("[yes/no]> ").lower()
							if n == 'yes':
								new_game.book_picker(self.scene)
							else:
								print("\nYou walk away from the bookshelf... not wanting to read a book")
						elif obj == 'chest':
							responses = [
								"You kick the chest... it doesn't do anything.",
								"You try to move the chest, but it appears to be bolted to the floor.",
								"You sit on the chest. Your butt is kinda uncomfy so you stand yet again."
							]
							print(random.choice(responses))
						elif obj == 'counter':
							print(shop_stock)
							print("What do you want to buy?")
							item = input("[apple/key]> ").lower()
							while item != 'apple' and n != 'key':
								print("Enter 'apple' or 'key'...")
								print("What do you want to buy?")
								item = input("[apple/key]> ").lower()
							if item == 'apple':
								print("How many apples do you want to buy?")
								n = int(input("[int]> "))
								while n < 0 or n > self.scene.stock['apple'] or (n*self.scene.prices['apple']) > user.gold:
									print("You cannot buy that many...")
									print('How many do you want to buy?')
									n = int(input("[int]> "))
								user.inventory['apple'] += n
								self.scene.stock['apple'] -= n
								user.gold -= (n * self.scene.prices['apple'])
							else:
								print("How many keys do you want to buy?")
								n = int(input("[int]> "))
								while n < 0 or n > self.scene.stock['key'] or (n*self.scene.prices['key']) > user.gold:
									print("You cannot buy that many...")
									print('How many do you want to buy?')
									n = int(input("[int]> "))
								user.inventory['key'] += n
								self.scene.stock['key'] -= n
								user.gold -= (n * self.scene.prices['key'])
							print("\nYay! You bought {} {}(s) for {} gold!".format(n, item, n*self.scene.prices[item]))
							print("You now have {} apple(s) and {} gold.".format(user.inventory['apple'], user.gold))
						elif obj == 'door':
							responses = [
								"You kick the door but it doesn't budge. Sad, you thought it would be cool to finally kick through a door.",
								"You walk up to the door, but forget to stop moving. Your nose meets the door first, then you stomach and toes, finally your entire body is pressed against the door. Crushed it!",
								"You open the door. You slam the door. You open the door. You slam the door. You open the door. You slam the door. You open the door. You gently closed the door. Plot twist!"
							]
							print(random.choice(responses))
						elif obj == 'key':
							if self.scene.key_found:
								print("you took the key already...")
							else:
								self.scene.key_found = True
								print("You picked up the key.")
								user.inventory['key'] += 1
						elif obj == 'painting':
							if self.scene.title == 'bedroom':
								if self.scene.painting_moved:
									print("You look at your smashed painting, wishing that you hadn't done that. Too bad, you don't have the power to travel back in time...yet")
								else:
									self.scene.painting_moved = True
									print("You grab the painting of you and your mother off the wall and slam it to the ground. The wood frame cracks, warping the painting. Behind the painting, there is nothing but a wall and the nail it was hanging on. Sad, you just broke your painting...")
							if self.scene.title == 'kitchen':
								if self.scene.painting_moved:
									print("You notice that the painting is still not straight. Frustrated, you grab the painting and put on the table, calming your nerves.")
								else:
									self.scene.painting_moved = True
									print("You notice that the painting is slightly askew. Being the perfectionist that you are, you try to correct it. Suddenly, a key falls out from behind it, dropping to the floor. You pick up the key.")
									user.inventory['key'] += 1
						elif obj == 'path':
							if self.scene.title == 'polaris':
								print("You walk towards the cottage, excited to see what is inside.")
								self.next_scene = 'cottage'
							if self.scene.title == 'cottage':
								print("You exit the cottage and go back to your drop site.")
								self.next_scene = 'polaris'
							if self.scene.title == 'waterfall' or self.scene.title == 'cliff':
								print("You continue walking, soon coming to an open area.")
								self.next_scene = 'boss'
							if self.scene.title == 'boss':
								if new_game.map.tundra:
									print("You leave the area and head back to the cliff. You are now safe from the monster.")
									self.next_scene = 'cliff'
								else:
									print("You run from the sasquatch, opting to hide near the waterfall instead.")
									self.next_scene = 'waterfall'
						elif obj == 'portal':
							if self.scene.open_portal:
								print("You walk up to the portal, amazed by the swirling blue vortex. A note nearby says that the portal is only one-way, meaning once you go through, you can never go back.")
								print("\nAre you sure that you want to go through the portal?")
								n = input("[yes/no]> ")
								while n != 'yes' and n != 'no':
									print("Enter 'yes' or 'no'...")
									print("\nAre you sure you want to go through the portal?")
									n = input('[yes/no]> ')
								if n == 'yes':
									self.next_scene = new_game.path_picker()
								else:
									print("Y\nou back away from the portal, scared of its power.")
							else:
								print("you cannot interact with this...")
						elif obj == 'refrigerator':
							if self.scene.title == 'kitchen':
								print("You grab a marker from the counter and draw a smiley face on your refrigerator. You smile at it. It smiles back.")
						elif obj == 'sofa':
							if self.scene.title == 'basement':
								print("You sit down on the sofa, resting for a little bit. curious, you search the couch cushions and find two spare keys. YAY what a great find!")
								user.inventory['key'] += 2
							if self.scene.title == 'cottage':
								print("You rest on the sofa, catching up on some sleep... but you soon wake up, compelled by an unknown force to finish the adventure.")
						elif obj == 'staircase':
							if self.scene.title == 'basement':
								print("You walk back up the staircase and open the back of the frigerator. It still wows you!")
								self.next_scene = 'kitchen'
						elif obj == 'trail':
							if self.scene.title == 'selva':
								print("You walk towards the hut, wondering what is inside.")
								self.next_scene = 'hut'
							if self.scene.title == 'hut':
								print("You exit the hut, wanting to go back to your drop site.")
								self.next_scene = 'selva'
							if self.scene.title == 'shop':
								if new_game.map.tundra:
									print("You walk out of the shop... pockets full after buying stuff.")
									self.next_scene = 'cliff'
								else:
									print("You walk out of the shop, intrigued by the loud roar of a waterfall nearby.")
									self.next_scene = 'waterfall'
							if self.scene.title == 'cliff' or self.scene.title == 'waterfall':
								print("You walk back towards the shop.")
								self.next_scene = 'shop'
						elif obj == 'tree':
							if self.scene.title == 'cliff':
								if self.scene.tree_picked == False:
									print('Luckily, this tree happens to be an apple tree! You pick the fruit and gain 8 apples. YAY!')
									user.inventory['apple'] += 8
									self.scene.tree_picked = True
								else:
									print("The tree has no more apples... :(")
						elif obj == 'tv':
							if self.scene.title == 'hut':
								print("You want to watch tv but can't find the remote. Oh well...")
						elif obj == 'window':
							responses = [
								"You tap on the glass and it cracks. You decide not to tap the glass anymore...",
								"You push on the window but it holds still. You have a very sturdy window.",
								"You look out the window at the nearby tree, wondering what it would be like to be a bird..."
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
						if obj == 'bed':
							print("Bed: a comfy place where you can lay down and stay down for the entire day.")
						elif obj == 'bookcase':
							print('Bookcase: a place to store books and other various items, like snowglobes or picture frames or trophies.')
						elif obj == 'chest':
							print('Chest: a body part OR a box that sometimes holds treasure.')
						elif obj == 'counter':
							print("Counter: a place where you can purchase items.")
						elif obj == 'door':
							print('Door: a block of material that separates two rooms.')
						elif obj == 'painting':
							print('Painting: something pricey, something artistic, something decorative.')
						elif obj == 'path':
							print("Path: a road-like thing that leads to somewhere else.")
						elif obj == 'refrigerator':
							print('Refrigerator: a cool place to store food or anything else you desire.')
						elif obj == 'sofa':
							print('Sofa: a comfortable sitting place where lots of items are lost between the cushions.')
						elif obj == 'trail':
							print("Trail: something road-like that can lead to somewhere else.")
						elif obj == 'tree':
							print("Tree: something brown... something green... something sometimes tall... something that needs water and sunlight.")
						elif obj == 'tv':
							print("TV: an entertainment device that shows tv shows and movies.")
						elif obj == 'window':
							print('Window: a place to look longingly at the outdoors.')
						else:
							print("you cannot look at this...")
					else:
						print("you cannot look at this...")
				elif 'm' in check_action or 'map' in check_action:
					unlocked_scenes = []
					for scene in new_game.map.scenes:
						scene = new_game.map.scenes.get(scene)
						if scene.visits >= 1:
							unlocked_scenes.append(scene.title)
						else:
							unlocked_scenes.append("?")
					if new_game.map.tundra:
						for scene in new_game.map.tundra_scenes:
							scene = new_game.map.tundra_scenes.get(scene)
							if scene.visits >= 1:
								unlocked_scenes.append(scene.title)
							else:
								unlocked_scenes.append("?")
					if new_game.map.jungle:
						for scene in new_game.map.jungle_scenes:
							scene = new_game.map.jungle_scenes.get(scene)
							if scene.visits >= 1:
								unlocked_scenes.append(scene.title)
							else:
								unlocked_scenes.append("?")
					for title in unlocked_scenes:
						print("{} => ".format(title.title()), end="")
					print('?', end="")
					print('')
				elif 'o' in check_action or 'open' in check_action:
					if obj in self.scene.objects:
						if obj == 'door':
							if self.scene.door_unlocked == False:
								print("the door is locked...")
							else:
								if self.scene.title == 'bedroom':
									print("You push the door open and look into the kitchen. You walk through the doorway.")
									self.next_scene = 'kitchen'
								if self.scene.title == 'kitchen':
									print("You push the door open, staring back at your bedroom. You walk through the doorway.")
									self.next_scene = 'bedroom'
								if self.scene.title == 'cottage' or self.scene.title == 'hut':
									print("You push the door open and enter the shop.")
									self.next_scene = 'shop'
								if self.scene.title == 'shop':
									if new_game.map.tundra:
										print("You open the door and look back at the cottage. You walk through the doorway.")
										self.next_scene = 'cottage'
									else:
										print("You open the door and look at the hut. You walk through the doorway.")
										self.next_scene = 'hut'
						elif obj == 'chest':
							if self.scene.chest_unlocked == False:
								print("the chest is locked...")
							else:
								if self.scene.chest_opened:
									print("You open the chest and realize you have already taken the contents...")
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
										user.gold += 5
										print('huzzah... another key and 5 gold!')
									if self.scene.title == 'cottage':
										user.inventory['apple'] += 3
										user.inventory['key'] += 2
										user.gold += 5
										print("WOOOOOOOO... you found 3 apples, 5 gold, and 2 keys!")
									if self.scene.title == 'hut':
										user.inventory['apple'] += 3
										user.inventory['key'] += 2
										user.gold += 5
										print("WOOOOOOOO... you got 3 apples, 5 gold, and 2 keys!")
									if self.scene.title == 'waterfall':
										user.inventory['apple'] += 8
										print("YAYYYYY.... 8 apples...")
									self.scene.chest_opened = True
						elif obj == 'refrigerator':
							if self.scene.title == 'kitchen':
								if self.scene.refrigerator_unlocked:
									print("You climb into the refrigerator and push open the back, revealing a staircase. Wow!")
									self.next_scene = 'basement'
								else:
									print("You open the refrigerator, but only find a moldy apple and some rotten cheese... Upon closer inspection, you notice a tiny keyhole on the back wall of the refrigerator. Interesting...")
						elif obj == 'window':
							if self.scene.title == 'bedroom':
								print("You open the window and jump out. Unfortunately, you forgot that you were on the third story and fell down into thorny bushes.")
								user.alive = False
								self.next_scene = 'death'
							if self.scene.title == 'kitchen':
								print("You opened the window and a small bird flew inside. It sung a little song. A few minutes later, it flew out again. Then you closed the window.")
							if self.scene.title == 'basement':
								print("You open the window and look outside. You can see ants marching past the window and some grass nearby. Suddenly, a bug flies right into your face. You close the window and wipe the bug off of your face. Bleh!")
						else:
							print("you cannot open this...")
					else:
						print('you cannot open that...')
				elif 'p' in check_action or 'profile' in check_action:
					user.print_ui()
				elif 'q' in check_action or 'quit' in check_action:
					clear()
					for x in range(random.randint(10,30)):
						print("Quitting.{}".format('.'*x))
						clear(0.5)
					sys.exit("Thank you for playing! Goodbye!")
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
									print('You unlocked the door!')
								else:
									print("you already unlocked the door... open it instead")
							elif obj == 'chest':
								if self.scene.chest_unlocked == False:
									self.scene.chest_unlocked = True
									user.inventory['key'] -= 1
									print('You unlocked the chest. Open it!')
								else:
									print("the chest is already unlocked... open it instead.")
							elif obj == 'refrigerator':
								if self.scene.refrigerator_unlocked == False:
									self.scene.refrigerator_unlocked = True
									user.inventory['key'] -= 1
									print("You insert your key into the small keyhole in the back. You turn the key and hear a lock click open. What could be behind the refrigerator?")
								else:
									print("you already unlocked the refrigerator... open it instead!")
							else:
								print('you cannot unlock that...')
					else:
						print('you cannot unlock that...')
				else:
					print("I don't know what you want me to do... :(")
		cont()

#finally... the actual game :)
user = None
new_game = Game()
new_game.start()
