import random, time, os, shelve, math, textwrap
import tkinter as tk

'''plan for game:
- !!!!! extend the story (actually have endings and stuff)
- !!! improve the shop
- ! maybe have a battle interface (show both user and monster atk and hp values)
- other ideas that come to me.....
'''

'''
TO DO LIST:
- 
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
	backpack (b) [item]: see inside your inventory OR see current quantity of an item
	consume (c) [item]: drink item or eat food
	discard (d) [item]: throw an item away
	erase (e) [item]: clears the terminal window
	go (g) [scene]: go to a scene
	help (h): view the help menu
	interact (i): interact with an object
	look (l): see an object's function
	map (m): see the scenes
	open (o) [item]: open object (chest/door)
	profile (p): view user profile
	scan (s): scans the room for interactable objects
	take (t) [item]: take object (key)
	use (u) [item]: use an item (key)
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
			self.atk = random.randint(1,30)
			self.reward = [30, 30] #[gold,xp]
		else: #extreme
			self.hp = random.randint(150,600)
			self.atk = random.randint(1,50)
			self.reward = [50, 50] #[gold,xp]

class User:
	classes = ['peasant', 'wizard', 'warrior', 'tank', 'gambler']
	hp = {'peasant': 100, 'wizard': 80, 'warrior': 70, 'tank': 150, 'gambler': random.randint(50, 170), 'god': 10000000000}
	atk = {'peasant': 50, 'wizard': 80, 'warrior': 100, 'tank': 30, 'gambler': random.randint(10, 120), 'god': 10000000000}
	xp_requirement = [100, 100, 100, 100, 100, 150, 150, 150, 175, 175, 200, 200, 250, 250, 300] #total of 15 levels at the moment
	# beginner_quests = ['Get 50 gold', 'Kill 5 monsters', 'Reach [2nd scene]', '']
	# quest_rewards = [[0,50], [50, 0], [100, 100], []] #[gold, xp]

	def __init__(self):
		self.inventory = {'apple': 0, 'chestplate': 0, 'helmet': 0, 'key': 0, 'pants': 0, 'potion': 0, 'shoes': 0, 'water': 0}
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
			print("\nEnter the name of a class!")
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
		print("[SYSTEM]: Are you sure you want to battle?")
		n = input("[yes/no]> ")
		while n != 'yes' or n != 'no':
			print("[SYSTEM]: ERROR")
			print("[SYSTEM]: Are you sure you want to battle?")
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
		self.objects = ['chest', 'door', 'key', 'painting', 'bed']
		self.next_scene = 'kitchen'
		self.visits = 0
		self.repeat_messages = [
			'You walk into the bedroom and see that everything has been cleaned. Your bed is made, the floor has no clothes, and your windows are no longer dusty. You wonder who could have done this...',
			'You enter your bedroom and everything is the same. The specimen is still hiding in the closet.',
			'The bedroom looks the same, except you understand that everything has been replaced with an exact replica. Well, the specimen is gone so... not everything.'
		]
	def play(self, mode='repeat'):
		if mode == 'repeat':
			new_game.story['text'] = random.choice(self.repeat_messages)
		else:
			new_game.story['text'] = "You slowly open your eyes, squinting at the bright light shining through your window. You look at your watch, reading that it's 8:07 AM. You get up and get dressed. You walk over to your bedroom door, only to discover that it is locked."

class Kitchen(Scene):
	def __init__(self):
		self.title = "kitchen"
		self.next_scene = 'basement'
		self.visits = 0
		self.repeat_messages = [
			'You walk into the kitchen yet again, wondering why you came back...',
			'You enter the kitchen, hoping to make a grilled cheese sandwich. Sadly you have no cheese so your plans are ruined.',
			'In the kitchen, you open the refrigerator. Inside is a rotten apple and a moldy tin of tomatoes. Too bad.'
		]
		self.objects = ['door', 'chest', 'painting', 'refrigerator']

class Basement(Scene):
	def __init__(self):
		self.title = "basement"
		self.visits = 0
		self.repeat_messages = [
			'You walk back down into the basement, still in awe it was hidden from you for your entire life.',
			'You start walking down the stairs but accidentally stumble and fall, landing hard on the concrete floor. Ouch.',
			'You rush down the stairs in a hurry. After a few seconds, you stop. Why were you in such a hurry?'
		]
	def play(self, mode='repeat'):
		if mode == 'repeat':
			print(random.choice(self.repeat_messages))
		else:
			print(textwrap.dedent("""
			
			"""))

class Polaris(Scene):
	def __init__(self):
		self.title = "polaris"
		self.visits = 0

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
		'polaris': Polaris()
	}
	jungle_scenes = {
		'scene': Scene()
	}

	def __init__(self, first_scene='bedroom'):
		self.tundra = False
		self.jungle = False
		self.first_scene = Map.scenes.get(first_scene)

class Game:
	items = {
		'apple': 'atk +5',
		'chestplate': 'dmg -20%',
		'helmet': 'dmg -15%',
		'key': 'usable to unlock doors and chests',
		'pants': 'dmg -10%',
		'potion': 'restores 50% of lost health',
		'shoes': 'dmg -5%',
		'water': 'restores 5 hp'
	}
	def __init__(self, mapobj):
		self.map = mapobj
		self.cur_scene = self.map.first_scene
		
		#TKINTER :(
		self.window = tk.Tk()
		self.window.title("The Wanderer")
		self.window.bind("<Return>", self.print_ui)
		# self.window.bind("<a>", self.print_ui)

		self.help_menu = tk.Frame(master=self.window)
		self.help_menu.pack(fill=tk.X)
		self.lbl = tk.Label(master=self.help_menu, text="HELPFUL COMMANDS")
		self.lbl.pack(side=tk.LEFT)
		self.button = tk.Button(master=self.help_menu, text="show", command=self.click)
		self.button.pack(side=tk.RIGHT)
		self.text = tk.Text(master=self.help_menu)
		self.text.pack(fill=tk.X)

		self.story_text = "This is the bedroom. You wake up and get dressed. You walk over to your bedroom door but it is locked. What are you going to do?"
		self.game = tk.Frame(master=self.window)
		self.game.pack(fill=tk.X, padx=(10,10))
		self.story = tk.Label(master=self.game, text=self.story_text)
		self.story.pack()

		self.profile = tk.Frame(master=self.window)
		self.profile.pack(fill=tk.X, padx=(10,10))
		self.user = tk.Text(master=self.profile)
		self.user.pack()

		self.input = tk.Frame(master=self.window)
		self.input.pack(fill=tk.X, padx=(10,10))
		self.entry = tk.Entry(master=self.input)
		self.entry.pack(fill=tk.X)

		self.console_text = "CONSOLE"
		self.output = tk.Frame(master=self.window, relief=tk.SUNKEN)
		self.output.pack(fill=tk.X, padx=(10,10))
		self.console = tk.Label(master=self.output, text=self.console_text)
		self.console.pack(padx=(10,10))

		self.window.mainloop()

	def click(self):
		if self.button['text'] == 'show':
			self.button['text'] = 'hide'
			self.text.delete('1.0', tk.END)
			self.text.insert('1.0', help_menu)
		else:
			self.button['text'] = 'show'
			self.text.delete('1.0', tk.END)
	def key_pressed(self, e):
		self.console['text'] = self.entry.get()
		self.entry.delete(0, tk.END)
	def print_ui(self, e):
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
		self.user.insert(tk.END, '{0}'.format('-' * max_char))
		mid_space = 0
		end_space = 0
		while (s1_sum + mid_space + end_space) < (s1_sum + s1_spaces):
			if (s1_sum + mid_space + end_space) + 2 > (s1_sum + s1_spaces):
				end_space += 1
			else:
				mid_space += 2
		self.user.insert(tk.END, "\n| {0} {4}| Level: {1} ({2}/{3}) {4}{5}|".format(user.name, user.lvl, user.xp, User.xp_requirement[user.lvl], mid_space//2*' ', end_space*' '))
		self.user.insert(tk.END, '\n|{0}|'.format('-'*(max_char-2)))
		mid_space = 0
		end_space = 0
		while (s2_sum + mid_space + end_space) < (s2_sum + s2_spaces):
			if (s2_sum + mid_space + end_space) + 3 > (s2_sum + s2_spaces):
				end_space += 1
			else:
				mid_space += 3
		self.user.insert(tk.END, "\n| HP: {0}/{1} {4}| ATK: {2} {4}| Gold: {3} {4}{5}|".format(user.hp, user.maxhp, user.atk, user.gold, mid_space//3*' ', end_space*' '))
		self.user.insert(tk.END, '\n{0}'.format('-' * max_char))
		cont()
	def view_inventory():
		clear(1)
		inv = user.inventory
		title("{}'s Inventory:\n".format(user.name))
		for key in inv:
			if inv[key] != 0:
				print("""{}: {}""".format(key, inv[key]))
				time.sleep(0.5)
		user.inventory = inv

		cont()

class Parser:
	def __init__(self, cur_scene):
		self.scene = cur_scene
		self.next_scene = None

	def handle_action(self, user_input):
		while self.next_scene == None:
			action = user_input
			if action != "":
				check_action = action.split()
				obj = check_action[-1]
				if 'a' in check_action or 'attack' in check_action:
					if obj in self.scene.monsters.keys():
						Battle(user, self.scene.monsters.get(obj))
					else:
						new_game.output_text.set("you cannot attack this monster...")
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
								print("your atk has been raised by 10 points!")
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
						if obj == self.scene.next_scene or obj == self.scene.prev_scene:
							self.next_scene = obj
						else:
							print("you cannot go here...")
					else:
						print("you cannot go here...")
				elif 'i' in check_action or 'interact' in check_action:
					if obj == 'refrigerator' and self.scene.title == 'kitchen':
						print("You move the refrigerator to the side, ")
				elif 'l' in check_action or 'look' in check_action:
					if obj in Game.items:
						print(Game.items[obj])
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
				elif 'o' in check_action or 'open' in check_action:
					if obj == 'door':
						if self.scene.door_unlocked:
							print("you opened the door!")
							self.next_scene = Bedroom.next_scene
						else:
							print("the door is locked...")
					elif obj == 'chest':
						if self.scene.chest_unlocked:
							print("you opened the chest!")
							if self.scene.chest_opened:
								print("you open the chest and realize you have already taken the contents...")
							else:
								self.scene.chest_opened = True
								print("wow... you found 15 gold and another key")
								user.gold += 15
								user.inventory['key'] += 1
					else:
						print("you cannot open that...")
				elif 'p' in check_action or 'profile' in check_action:
					print_ui()
				elif 's' in check_action or 'scan' in check_action:
					print("\nInteractable Objects:")
					for item in self.scene.objects:
						print("[-] {}".format(item))
				elif 't' in check_action or 'take' in check_action:
					print("you took a(n) {}...".format(obj))
					if obj == 'key':
						self.scene.key_found = True
						user.inventory['key'] += 1
					else:
						print("you cannot take that...")
				elif 'u' in check_action or 'use' in check_action:
					if obj == 'key':
						if self.scene.key_found:
							choice = input("[chest/door/refr]> ")
							if choice == "chest":
								print("you unlocked the chest!")
								self.scene.chest_unlocked = True
							elif choice == "door":
								print("you unlocked the door!")
								self.scene.door_unlocked = True
							else:
								print("oops. you accidentally swallowed your key...")
							user.inventory['key'] -= 1
						else:
							print("you don't have a key...")
					else:
						print("you cannot use that...")
		cont()

#finally... the actual game :)
user = User()
new_map = Map()
new_game = Game(new_map)
new_game.start()