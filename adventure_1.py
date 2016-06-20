# text-based adventure game

from Place import Place
from Item import Item, Key, Food


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
	for i in new_place.items_inside:
		ask_to_take(i, new_place)
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
		inventory.append(item)
		new_place.remove_item(item)
		


inventory = []
commands = ["n", "s", "e", "w", "i", "c"]
placeIdDict = {}

purple_key = Key("pk", "Purple key")
blue_key = Key("bk", "Blue key")
orange_key = Key("ok", "Orange key")
peach_key = Key("pek", "Peach key")

placeIdDict["mir"] = Place("mir", "Mirror Room", "A lot of mirrors, four doors", [], ["red", "pin", "gre", "cak"], [None, None, [orange_key], [purple_key]])
placeIdDict["red"] = Place("red", "Red Room", "The walls are all red... blood?", [blue_key], [None, "mir", "aqu", None], [])
placeIdDict["aqu"] = Place("aqu", "Aqua Room", "You are drowning...", [peach_key], [None, None, None, "red"], [])
placeIdDict["pin"] = Place("pin", "Pink Room", "Fluffy pink walls :D", [orange_key], ["mir", None, None, None], [])
placeIdDict["gre"] = Place("gre", "Green Room", "Slimy", [], [None, "yel", None, "mir"], [None, [blue_key, orange_key], None, [orange_key]])
placeIdDict["yel"] = Place("yel", "Yellow Room", "Pretty sunlight", [purple_key], ["gre", None, None, None], [[blue_key, orange_key], None, None, None])
placeIdDict["cak"] = Place("cak", "Cake Room", "You won!", [], [None, None, "mir", None], [None, None, [purple_key, peach_key], None])

##inventory.extend()


current_place = placeIdDict["mir"]
"""
print(valid_input("n"))
print(valid_input("s"))

current_place = move("n")
print(current_place.name)
print(inventory[0].name)
"""

print(current_place)
while True:
## game play
	##print(current_place.name)
	choice = input("Where do you want to go (n/s/e/w/i -view inventory /c -get current place description)? ")
	while not valid_input(choice):
		choice = input("Please enter n, s, e, w, i, or c: ")
	if choice == "i":
		display_inventory()
		continue	
	if choice == "c":
		print(current_place)
		for i in current_place.items_inside:
			ask_to_take(i, current_place)
		continue
	current_place = move(choice)
	##print (" You are in ", current_place.name)
	display_inventory()
	##print(current_place)
	print("___________________")
	if current_place == placeIdDict["cak"]:
		break

print("You won the game! congrats!")


	