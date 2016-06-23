##adventure 2, adding monsters, food , fights, ect. 

# text-based adventure game

from Place import Place
from Item import Item, Key, Food, Weapon
from Attack import Attack
from Being import Being, Monster

import random


def valid_input(word):
	if word in commands:
		return True
	else:
		return False
		
def can_enter(old_place, door, command):
	if len(door.locks) == 0:
		return True
	if command == "n":
		entrance = 1 # south
	elif command == "s":
		entrance = 0 # north
	elif command == "e":
		entrance = 3 #west
	elif command == "w":
		entrance = 2 #east
	#print(entrance)
	door_keys = door.locks[entrance]
	if not door_keys:
		return True
	ready_keys = []
	for obstacle in door_keys:
		if type(obstacle) == Monster:
			print("There is a monster in your way! It is a " + obstacle.name)
			won = fight(obstacle)
			if not won:
				return False
			door_keys.remove(obstacle)
			##door.locks[entrance].remove(obstacle)
			current_place.locks[commands.index(command)].remove(obstacle)
	if len(door_keys) == 0:
		return True
	print(len(door_keys), " item(s) are needed")
	key_choice = input("You can't get in. Would you like to try to use an item on this door? (y/n) ")
	while not (key_choice == "y" or key_choice == "n"):
		key_choice = input("Please input a valid answer, y or n. ")
	while key_choice != "n":
		display_inventory()
		key_choice = input("Pick an item. (1, 2, 3, etc...), type \"n\" to go back: ")
		if not key_choice.isdigit():
			return False
		if int(key_choice) - 1 < len(inventory):  ## check if in range
			if type(inventory[int(key_choice) -1]) != Key:
				print("That isn't a key...")
				continue
			##print (type(door_keys[0]))
			if inventory[int(key_choice) - 1] in door_keys:
				print("Getting closer... ")
				ready_keys.append(inventory[int(key_choice) - 1])
		if set(door_keys) == set(ready_keys):
			door.locks[entrance] = None
			current_place.locks[commands.index(command)] = None
			print("It worked! You're in! ")
			return True
	return False
			
def move(command):
	c = commands.index(command)
	#print (c)
	##if c >= 4:
	##	return current_place
	if not current_place.places_around[c]:
		print("There's a wall.")
		return current_place
	new_place = placeIdDict[current_place.places_around[c]]
	if not can_enter(current_place, new_place, command):
		##print("ENTRANCE ERROR")
		return current_place
	print(new_place)
	##print(len(new_place.items_inside))
	##print(new_place.items_inside)
	for item in list(new_place.items_inside):
		##print (new_place.items_inside[0].name)
		ask_to_take(item, new_place)
		##print("    Added an item")
	##print("Out of the for loop. why the fuck am I out of it")
	return new_place
	
def display_inventory():
	print("Inventory: ")
	for i in inventory:
		print(inventory.index(i)+1, ". ", i.name)
		
def ask_to_take(item, new_place):
	choice = input("Would you like to take "+ item.name+ "? (y/n) ")
	while not (choice == "y" or choice == "n"):
		choice = input("Please input a valid answer, y or n. ")
	if choice == "y":
		print("Adding item...")
		inventory.append(item)
		new_place.remove_item(item)
		if type(item) == Weapon:
			print("Adding attack...")
			add_attack(item)
		
def choose_and_attack(victim):
	display_attacks()
	key_choice = input("Pick an attack. (1, 2, 3, etc...), type \"n\" to go back: ")
	if not key_choice.isdigit():
		return False
	while not int(key_choice) - 1 < len(me.attacks):
		key_choice = input("Pick one of the numbers: ")
		if not key_choice.isdigit():
			return False
	if int(key_choice) - 1 < len(me.attacks):  ## check if in range
		attack(victim, me.attacks[int(key_choice) - 1])
		
def fight(monster):
	## should there be a set number of attacks/moves??
	while True:
		## player move
		# player chooses attack : display attacks, also option to run
		print("Choose an attack")
		choose_and_attack(monster)
		
		if monster.willingness <= 0 or monster.health_points <= 0 or me.willingness <= 0 or me.health_points <= 0:
			break
		print("___________")
		# monster move
		if monster.health_points <= 20 or monster.willingness <= 20:
			# monster starting to run away
			print(monster.name + " is hurt and starting to retreat! You have one last chance to defeat them.")
			choose_and_attack(monster)
			if monster.health_points > 0 and monster.willingness > 0:
				print("They were able to get away! Their power is restored slightly...")
				## restore monster power
				monster.health_points = 70
				monster.willingness = 70
				display_stats(monster)
				return False
			else:
				break
		
		attack(me, random.choice(monster.attacks))
		if monster.willingness <= 0 or monster.health_points <= 0 or me.willingness <= 0 or me.health_points <= 0:
			break
		print("___________")
		if me.health_points <= 10 or me.willingness <= 10:
			#offer choice to run away
			runaway = input("You're very weak, do you want to retreat? Type \"n\" if you'd like to continue fighting ")
			if runaway != "n":
				return False
	if monster.willingness <= 0 or monster.health_points <= 0:
		print("  You won!")
		return True ## you won!
	else:
		print("  You lost!")
		print(" You black out and wake up back where you started... ")
		current_place = placeIdDict["mir"]
		return False ## you lost
	
def add_attack(weapon):
	me.attacks.append(weapon.corresponding_attack)
	print(weapon.corresponding_attack.name + " was added to your attacks!")

def attack(victim, attack):
	print (victim.name + " was attacked with " + attack.name)
	## check for critical strike
	chance = random.random()
	if chance < P_critical_strike:
		print("Critical strike!")
		victim.willingness -= attack.compassion*2
		victim.health_points -= attack.power*2
	## check for miss
	elif chance >= P_critical_strike and chance < P_critical_strike+P_miss:
		print("The attack missed! ")
	else:
		victim.willingness -= attack.compassion
		victim.health_points -= attack.power
	display_stats(victim)
	
def display_stats(person):
	print(person.name + " stats: \nHP: " + str(person.health_points) + "\nWillingness: " +  str(person.willingness))
	
def display_attacks():
	print("Attacks: ")
	for i in me.attacks:
		print(me.attacks.index(i)+1, ". ", i.name)
	
def eat(food):
	print("Eating " + food.name)
	inventory.remove(food)
	me.health_points += food.calories
	if me.health_points > 100: ##set cap on HP
		me.health_points = 100
		
def choose_powerup():
	choice = input("Would you like to use any items (power-ups) right now? y/n ")
	while not (choice == "y" or choice == "n"):
		choice = input("Enter \"y\" or \"n\": ")
	while choice != "n":
		display_inventory()
		choice = input("Pick an item. (1, 2, 3, etc...), type \"n\" to go back: ")
		if not choice.isdigit():
			return False
		print(choice)
		if int(choice) - 1 < len(inventory):  ## check if in range
			if type(inventory[int(choice)-1]) == Food: ## if it's a food, go ahead
				eat(inventory[int(choice)-1])
			else:
				print("Sorry, you can't use that right now")
				continue
		else:
			print("Try again")
		
def generate_from_file(filename):
	## skip first line bc timestamp?
	count_large = 0
	with open(filename, 'r') as input:
		for line in input:
			##print (line)
			##print(count_large)
			if line.strip() == large_break:
				##print("MADE IT HERE")
				count_large += 1
				##print("New count_large: " + str(count_large))
				continue
			info = line.split(small_break)
			##print (info)
			if count_large == 0: ## timestamp
				print("Time" + line)
			elif count_large == 1:  ## key creation
				key = info[0]
				name = info[1]
				keyIdDict[key] = Key(key, name)
				allItemsDict[key] = keyIdDict[key]
			elif count_large == 2: ## Food creation
				key = info[0]
				name = info[1]
				description = info[2]
				calories = int(info[3])
				foodIdDict[key] = Food(key, name, description, calories)
				allItemsDict[key] = foodIdDict[key]
			elif count_large == 3: ## attack creation
				key = info[0]
				name = info[1]
				description = info[2]
				uses = int(info[3])
				hp = int(info[4])
				compassion = int(info[5])
				attackIdDict[key] = Attack(key, name, description, uses, hp, compassion)
			elif count_large == 4: ##weapon creation
				key = info[0]
				name = info[1]
				description = info[2]
				attack = attackIdDict[info[3]]
				weaponIdDict[key] = Weapon(key, name, description, attack)
				allItemsDict[key] = weaponIdDict[key]
			elif count_large == 5:  ## monster creation - 	HUMAN IS DONE SEPARATELY
				key = info[0]
				name = info[1]
				description = info[2]
				starterAttacks = info[3].split(tiny_break) ## just the id
				realAttacks = []
				for a in starterAttacks:
					realAttacks.append(attackIdDict[a])
				beingIdDict[key] = Monster(key, name, description, realAttacks)
				allItemsDict[key] = beingIdDict[key]
			elif count_large == 6:  ##place
				key = info[0]
				name = info[1]
				description = info[2]
				real_items = []
				if info[3]: ## if empty
					##print("Not empty")
					items_inside = info[3].split(tiny_break) ## just the item code
					for s in items_inside:
						real_items.append(allItemsDict[s]) ##finds item from allItemsDict and puts key/food/weapon object in real_items
				places_near = info[4].split(tiny_break)  ## only need the id (string)
				actual_places = []
				for p in places_near:
					if p:
						actual_places.append(p)
					else:
						actual_places.append(None)
				raw_locks = info[5].split(tiny_break) 
				real_locks = []
				for l in raw_locks:
					print(l)
					if not l: ## empty
						real_locks.append(None)
					else:
						if ',' in list(l):
							detail = l.split(',')
							for i in detail:
								real_locks.append(allItemsDict[i])
						else:				
							real_locks.append(allItemsDict[l])
				placeIdDict[key] = Place(key, name, description, real_items, actual_places, real_locks)
			else:
				##print ("This is the name: " + info[0])
				name = info[0][:3]
				##print (name)
				current_place = placeIdDict[name]
				##print(current_place)
				return current_place
				
def save_to_file(filename):
	pass
		

P_critical_strike = 0.05
P_miss = 0.04

name = input("Enter your name: ")

me = Being(0, name, "I am me", [])

##attacks


inventory = []
commands = ["n", "s", "e", "w", "i", "c", "h"]

	
placeIdDict = {}
keyIdDict = {}
attackIdDict = {}
foodIdDict = {}
weaponIdDict = {}
beingIdDict = {}
allItemsDict = {}

tiny_break = '*^'
small_break = '^%^'
large_break = '$#$'

current_place = generate_from_file("colorRoom1.txt")

for i in allItemsDict:
	print (allItemsDict[i].name)
	


"""
placeIdDict = {}
keyIdDict = {}
attackIdDict = {}
foodIdDict = {}
weaponIdDict = {}
beingIdDict = {}

##make sure 3-letter names don't overlap!

keyIdDict["puk"] = Key("puk", "Purple key")
keyIdDict["blk"] = Key("blk", "Blue key")
keyIdDict["ork"] = Key("ork", "Orange key")
keyIdDict["pek"] = Key("pek", "Peach key")

attackIdDict["sli"] = Attack("sli", "Slice", "swish", 1000, 40, 0)   ##when reading from file, will go through keyIdDict and attackIdDict when creating Places
attackIdDict["com"] = Attack("com", "Compassion", "Showers opponent with sympathy", 10000, 0, 50)
attackIdDict["sti"] = Attack("sti", "Sting", "Deadly sting", 10000, 30, 0)

weaponIdDict["swo"] = Weapon("swo", "Sword", "gives you the slice attack", attackIdDict["sli"])

foodIdDict["bre"] = Food("bre", "Loaf of Bread", "gives you health points!", 60)

me.attacks.append(attackIdDict["com"])
beingIdDict["sco"] = Monster("sco", "Deadly Scorpion", "Will probably kill you...", [attackIdDict["sti"]])



print (me.attacks)

## Place(str id, str name, str description, list of items inside, list of four connecting rooms in NSEW order, list of list of locks to adjacent rooms in NSEW order)
placeIdDict["mir"] = Place("mir", "Mirror Room", "A lot of mirrors, four doors", [], ["red", "pin", "gre", "win"], [None, None, [keyIdDict["ork"]], [keyIdDict["puk"]]])
placeIdDict["red"] = Place("red", "Red Room", "The walls are all red... blood?", [weaponIdDict["swo"], keyIdDict["blk"]], [None, "mir", "aqu", None], [None, None, [beingIdDict["sco"]], None])
placeIdDict["aqu"] = Place("aqu", "Aqua Room", "You are drowning...", [keyIdDict["pek"]], [None, None, None, "red"], [None, None, None, [beingIdDict["sco"]]])
placeIdDict["pin"] = Place("pin", "Pink Room", "Fluffy pink walls :D", [keyIdDict["ork"], foodIdDict["bre"]], ["mir", None, None, None], [])
placeIdDict["gre"] = Place("gre", "Green Room", "Slimy", [], [None, "yel", None, "mir"], [None, [keyIdDict["blk"], keyIdDict["ork"]], None, [keyIdDict["ork"]]])
placeIdDict["yel"] = Place("yel", "Yellow Room", "Pretty sunlight", [keyIdDict["puk"]], ["gre", None, None, None], [[keyIdDict["blk"], keyIdDict["ork"]], None, None, None])
placeIdDict["win"] = Place("win", "Cake Room", "You won!", [], [None, None, "mir", None], [None, None, [keyIdDict["puk"], keyIdDict["pek"]], None])

##inventory.extend()

#attack(scorpion, show_compassion)
#attack(me, sting)

#fight(scorpion)

current_place = placeIdDict["mir"]
"""

print(current_place)
while True:
## game play
	##print(current_place.name)
	choice = input("Where do you want to go (n/s/e/w/i -view inventory /c -get current place description /h -get your stats)? ")
	while not valid_input(choice):
		choice = input("Please enter n, s, e, w, i, c, or h: ")
	if choice == "i":
		display_inventory()
		choose_powerup()
		continue	
	if choice == "c":
		print(current_place)
		for i in current_place.items_inside:
			ask_to_take(i, current_place)
		continue
	if choice == "h":
		display_stats(me)
		continue
	current_place = move(choice)
	##print (" You are in ", current_place.name)
	##print(current_place)
	print("___________________")
	if current_place == placeIdDict["win"]:
		break
	display_inventory()

print("You won the game! congrats!")


	