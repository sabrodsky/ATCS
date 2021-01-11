import random, time, os

'''plan for game:
- !!!!! convert user variables into User class
- !!!!! extend the story (actually have endings and stuff)
- !!! improve the shop
- !!!! improve the user interface (i will make a little box that displays health, level and exp, and gold values)
- ! maybe have a battle interface (show both user and monster atk and hp values)
- !!!!! convert every single question function into a while loop
- other ideas that come to me.....
'''

#other stuff for adventure
monsters = ["a land-dwelling octopus", "an evil goblin", "a rabid puppy", "The Devil", "the most evil of ghosts", "a giant blob of slime (his name is Bob)", "a purple alien armed with a futuristic laser gun", "a talking tree", "a zombie", "a flying bear with two swords"]
monsterhp = random.randint(1,80)
monsteratk = random.randint(1, 5)

battleInitiated = False
userWon = True

userhp = 10
usermaxhp = 10
useratk = 10
userinventory = []
userlvl = 1
userexp = 0
usergold = 0

'''user class
peasant: hp 100; atk 50
wizard: hp 80; atk 80
warrior: hp 70; atk 100
tank: hp 150; atk 30
gambler: random stats
'''


#collection of answer functions
def question1(Specimen):
  n = input(Specimen + ": Would you like to go on an adventure? (y/n): ")
  if(n == "y"):
    x = "yes"
  elif(n == "n"):
    x = "no"
  else:
    print(Specimen + ": That is not an answer!")
    x = question1(Specimen);
  return x

def question2(Specimen):
  n = input(Specimen + ": Would you like to invite other people? (y/n): ")
  if(n == "y"):
    x = "yes"
  elif(n == "n"):
    x = "no"
  else:
    print(Specimen + ": That is not an answer!")
    x = question2(Specimen);
  return x

def question3(Specimen):
  n = input(Specimen + ": Which would you like to be? (peasant/wizard/warrior/tank/gambler): ")
  if(n == "peasant"):
    userhp = 100
    useratk = 50
    print(Specimen + ": You are now a peasant. Your hp is " + str(userhp) + " and your atk is " + str(useratk) + ".")
  elif(n == "wizard"):
    userhp = 80
    useratk = 80
    print(Specimen + ": You are now a wizard. Your hp is " + str(userhp) + " and your atk is " + str(useratk) + ".")
  elif(n == "warrior"):
    userhp = 70
    useratk = 100
    print(Specimen + ": You are now a warrior. Your hp is " + str(userhp) + " and your atk is " + str(useratk) + ".")
  elif(n == "tank"):
    userhp = 150
    useratk = 30
    print(Specimen + ": You are now a tank. Your hp is " + str(userhp) + " and your atk is " + str(useratk) + ".")
  elif(n == "gambler"):
    userhp = random.randint(50, 170)
    useratk = random.randint(10, 120)
    print(Specimen + ": You are now a gambler. Your hp is " + str(userhp) + " and your atk is " + str(useratk) + ".")
  elif(n == "god"):
    userhp = 1000000000000000000000000000000
    useratk = 1000000000000000000000000000000
    print(Specimen + ": You are now a god. Your hp is " + str(userhp) + " and your atk is " + str(useratk) + ".")
  else:
    print(Specimen + ": That is not an answer!")
    question3(Specimen)
  return [userhp, useratk]

def question4(Specimen):
  n = input(Specimen + ": Would you like to go left, straight, or right? (l/s/r): ")
  if(n == "l"):
    x = "left"
  elif(n == "s"):
    x = "straight"
  elif(n == "r"):
    x = "right"
  else:
    print(Specimen + ": That is not an answer!")
    x = question4(Specimen);
  return x

def question5(Specimen):
  n = input(Specimen + ": Would you like to use the potion or put it into your inventory? (use/keep): ")
  if(n == "use"):
    x = "use"
  elif(n == "keep"):
    x = "keep"
  else:
    print(Specimen + ": That is not an answer!")
    x = question5(Specimen)
  return x
    
def question6():
  n = input("Mayor: Will you help us get rid of the monster? (y/n): ")
  if(n == "y"):
    x = "yes"
  elif(n == "n"):
    x = "no"
  else:
    print("Mayor: That is not an answer!")
    x = question6()
  return x



#other functions
def gameOver():
  print("Congrats. You have died. Welcome to the game over part of this adventure. From here, you may only choose to end the game. Sorry :/")

def userLevelUp(lvl):
  maxhp = 5
  atk = lvl * 8

  return [maxhp, atk]

def battleMonster(userhp, useratk, monsterhp, monsteratk):
  time.sleep(10)
  os.system('clear')
  print("INITIATING BATTLE")
  for x in range(10, -1, -1):
    print(x)
    time.sleep(1)
    replit.clear
  print("BATTLE START\n\n")
  battleInitiated = True

  print("Monster HP: " + str(monsterhp) + "\nMonster ATK: " + str(monsteratk) + "\nYour HP: " + str(userhp) + "\nYour ATK: " + str(useratk) + "\n\n\n\n")
  time.sleep(3)

  while(battleInitiated):
    print("You hit the monster.")
    monsterhp -= useratk
    print("Monster has " + str(monsterhp) + " hp.\n")
    if(monsterhp <= 0):
      battleInitiated = False
      userWon = True
      break
    time.sleep(3)
    print("The monster swings at you.")
    userhp -= monsteratk
    print("You now have " + str(userhp) + " hp.\n")
    if(userhp <= 0):
      battleInitiated = False
      userWon = False
      break
    time.sleep(3)
  os.system('clear')
  return [userWon, userhp]

def battleAftermath(lvl, userexp):
  print("Narrator: Congratulations! You have defeated the monster! You have received 50 gold and 50 exp.")
  gold = 50
  userexp += 50
  maxhp = 0
  atk = 0
  while(userexp >= 100):
    newValues = userLevelUp(userlvl, userexp)
    lvl += 1
    maxhp = newValues[0]
    atk = newValues[1]
    userexp -= 100
    print("Narrator: You have leveled up! Your level is now " + str(lvl) + ", your new max hp is " + str(usermaxhp) + ", and your new atk is " + str(useratk) + ".")
  return [gold, userexp, maxhp, atk]
  
def shop(gold):
  n = int(input("Which item would you like to buy? (1/2/3/4/5): "))
  x = 0
  shoppingBag = []
  if(n == 1):
    shoppingBag.append("full health potion")
    gold -= 15
    x = 1
  elif(n == 2):
    shoppingBag.append("Armor")
    gold -= 30
    x = 1
  elif(n == 3):
    shoppingBag.append("Fighting Book")
    gold -= 10
    x = 1
  elif(n == 4):
    shoppingBag.append("War Book")
    gold -= 20
    x = 1
  z = shoppingBag.find("gold")
  if(z == 1):
    shoppingBag.pop(z)
  else:
    shoppingBag.append("gold: " + str(gold))
  if(x == 0):
    print("That is not an answer!")
    return shop(gold)
  else:
    g = input("Would you like to buy another item? (y/n): ")
    if(g == "y"):
      shop(gold)
    else: 
      print("Ok...")
  return shoppingBag

#assign specimen random number
value = random.randint(1, 10000)
Specimen = "Specimen " + str(value);

#introduce user
print("Narrator: You are sitting down at the table for breakfast, wondering what you'll do today. You're staring into your oatmeal when suddenly you hear a loud noise. There is smoke and dust clouding your view behind you. After a couple of seconds, it clears, leaving an odd figure in its place.\n")
time.sleep(12)
userName = input("Hello. I am " + Specimen + ". What is your name?\n")
print(Specimen + ": Welcome " + userName + "!")

#introduce user
userAge = int(input(Specimen + ": How old are you?\n"))
print(Specimen + ": Wow! That's awesome. I am " + str(random.randint(1000, 1000000)) + " years old.")

#start of adventure
answer1 = question1(Specimen);

#path of yes (adventure)
if(answer1 == "yes"):
  print(Specimen + ": Hooray! We're going to have so much fun!")

  print(Specimen + ": Ok. First order of business... should we invite other people on this adventure? As they say, the more the merrier!")

  #inviting people
  answer2 = question2(Specimen);
  
  #path of yes (adventure, people)
  if(answer2 == "yes"):
    friendName = input(Specimen + ": Alrighty! Who do you want to invite?\n")
    print(Specimen + ": Great! Let's go get them!")
    for x in range(20):
      time.sleep(0.5)
      print(".")
    print(Specimen + ": Welcome " + friendName + "!")
  #path of no (adventure, solo)
  elif(answer2 == "no"):
    print(Specimen + ": Ok. No worries! We'll go solo!")

  #assigning user a role (doesn't include accompanying friend because that would suck)
  time.sleep(2)
  print(Specimen + """: Alright. Next order of business... you must choose your role. You can be a peasant, wizard, warrior, tank, or gambler. Each come with their own health points (hp) and attack points (atk).
    Peasant: hp = 100; atk = 50
    Wizard: hp = 80; atk = 80
    Warrior: hp = 70; atk = 100
    Tank: hp = 150; atk = 30
    Gambler: hp and atk points are random
  """)
  
  answer3 = question3(Specimen);
  userhp = answer3[0]
  useratk = answer3[1]
  usermaxhp = answer3[0]

  #choosing paths (left, straight, right)
  time.sleep(5)
  os.system('clear')
  print("Narrator: You exit the house and walk into the woods. Soon you find a fork in the road (I know, cheesy). This fork has three different paths.")

  answer4 = question4 (Specimen);
  os.system('clear')
  #path of yes (adventure, __, left)
  if(answer4 == "left"):
    print("Narrator: You turn left and continue walking.")

  #path of yes (adventure, __, straight)
  if(answer4 == "straight"):
    print("Narrator: You decide straight is best and continue walking forward.")

  #path of yes (adventure, __, right)
  if(answer4 == "right"):
    print("Narrator: You thought that the right path was the right way to go (haha). You continue towards the right path.")

  #something blocks the path!
  print("Narrator: You walk for a little while, bored out of your mind. Suddenly, " + monsters[random.randint(0, len(monsters) - 1)] + " appears on the path in front of you. It blocks your path so you must fight. Luckily, the player is allowed to hit first. When your hp hits 0, it's game over. Make sure you keep your hp up and upgrade your atk often.\n\nOne way to do that is to level up. You get experience points (exp) after defeating monsters, and once you have one hundred exp, you level up. When you level up, your max hp is upgraded and your atk is upgraded. Your health is also reset! You may also use gold (also acquired from defeating monsters) in shops to buy upgrades. Good luck!\n\n")
  
  battleResults = battleMonster(userhp, useratk, monsterhp, monsteratk);

  userWon = battleResults[0]
  userhp = battleResults[1]

  #path of yes (adventure, __, __, monster killed by you)
  if(userWon):
    print(Specimen + ": You have defeated the monster! You have been awarded 50 gold and 100 exp. Great job! Due to your success, I will award you with a potion. At the moment, your hp is " + str(userhp) + ". This potion resets your hp. You may only use it before initiating a battle or after you have won a battle.")
    usergold += 50
    userexp += 100
    
    if(userexp >= 100):
      newValues = userLevelUp(userlvl)
      usermaxhp += newValues[0]
      useratk += newValues[1]
      userlvl += 1
      userexp = newValues[2]

    answer5 = question5(Specimen)

    #use potion
    if(answer5 == "use"):
      userhp = usermaxhp
      print(Specimen + ": Great! Your hp is now " + str(userhp))
    #save potion
    elif(answer5 == "keep"):
      userinventory.append("full health potion")
      print(Specimen + ": Great! Your hp is still " + str(userhp) + " and you have a 'full health potion' in your inventory\n\n")
      print("Your inventory: " + str(userinventory))
    time.sleep(5)
    os.system('clear')
    print("Narrator: You continue walking down the path, excited that you have won your first battle. Up ahead, you see that the path opens into a small town. Some townspeople are gathered at a billboard set up in the center. You look at the board and see a lot of missing person reports. You ask what is going on.\n\nRandom citizen: Every night, a monster comes and takes a person away. We have tried curfews and locking our doors but it still manages to nab somebody. Please help us!\n\nMayor: If you help us, kind soul, you will receive a great reward.")

    answer6 = question6()
    
    #path of yes (yay helping people)
    if(answer6 == "yes"):
      print("Mayor: Great! I will lead you to the monster's hiding place. You will battle it, and if you win, we shall reward you. Follow me.")
      os.system('clear')
      battleResults = battleMonster(userhp, useratk, monsterhp, monsteratk);

      userWon = battleResults[0]
      userhp = battleResults[1]

      battleAftermath = battleAftermath(userlvl, userexp)

      usergold += battleAftermath[0]
      userexp = battleAftermath[1]
      userlvl += 1
      usermaxhp += battleAftermath[2]
      useratk += battleAftermath[3]

      print("Mayor: Thank you for defeating the monster! In addition to your battle rewards, I want to give you a few things. The first is a full health potion. The second is a free atk upgrade potion. It will increase your atk by 10 points. The final gift is the chance to go into our local shop. You may find some helpful upgrades or potions so don't forget to stop by.\n")
      useratk += 10
      print("Narrator: You drink the atk upgrade potion, increasing your atk by 10 points. Your atk is now " + str(useratk) + ".")

      answer7 = question5(Specimen);

      if(answer7 == "use"):
        userhp = usermaxhp
        print("Your health is now " + str(userhp))
      elif(answer7 == "keep"):
        userinventory.append("full health potion")
        print("Your health is " + str(userhp))

      print("\nNarrator: You walk over to the shop and enter the building. Inside, you see items.\n")
      print("""
        1) Full Health Potion | 15 Gold
        2) Armor (+50 HP) | 30 Gold
        3) Fighting Book (+20 ATK) | 10 Gold
        4) War Book (+40 ATK) | 20 Gold
      """)

      shoppingBag = shop(usergold, userinventory)

      usergold = shoppingBag[0]
      userinventory = shoppingBag[1]
    
    #path of yes (no helping people)
    elif(answer6 == "no"):
      print("Mayor: Oh well. Goodbye, stranger.")
  
  #path of yes (adventure, __, __, killed by monster)
  elif(not userWon):
    print("Narrator: The monster delivers a defeating blow, killing you. You have died. Better luck next time.")
    time.sleep(3)
    gameOver()

#path of no (adventure)
elif(answer1 == "no"):
  print(Specimen + ": Sad. I guess the adventure ends here.")