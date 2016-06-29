#items class 

class Item:
	def __init__(self, id, name, type, description, unlimited):
		self.id = id #string, three letters long
		self.name = name #string
		self.type = type #string like "key"
		self.description = description #string
		self.unlimited = unlimited #boolean
		
	def __str__(self):
		str = "%s, which is a %s that %s" % (self.name, self.type, self.description)
		##str = self.name + ", which is a " + self.type + " that " + self.description
		##print (str)
		return str
		
		
class Key(Item):
	def __init__(self, id, name):
		super(Key, self).__init__(id, name, "key", "unlocks some door...", True)
		##Item.__init__(self, id, name, "key", "unlocks some door...", True)
		
	def __str__(self):
		return super(Key, self).__str__()
		
		
class Food(Item):
	def __init__(self, id, name, description, calories, motivation):
		Item.__init__(self, id, name, "food", description, False)
		self.calories = calories
		self.motivation = motivation

class Weapon(Item):
	def __init__(self, id, name, description, corresponding_attack):
		super(Weapon, self).__init__(id, name, "weapon", description, True)
		self.corresponding_attack = corresponding_attack
		