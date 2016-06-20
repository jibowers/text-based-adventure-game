class Place:

	##keyToError = {"l": "Sorry, this door is locked."}
	def __init__(self, id, name, description, items_inside, places_around, locks):
		self.name = name #a string
		self.id = id #int, probably in order created (within main program)
		self.description = description #string
		self.items_inside = items_inside #list of Item objects, null if none
		##self.entrance_key = entrance_key #list of Items object needed to enter (ie. a key)
		self.places_around = places_around #list of place id's (int) it connects to in order: N, S, E, W
		"""if len(entrance_key) != 0:
			if entrance_key[0].type == "key":
				self.errorMessage = "Sorry, this door is locked."
				"""
		self.locks = locks # items needed to enter from N, S, E, W
		
	def remove_item(self, item):
		self.items_inside.remove(item)
		
	def add_item(self, item):
		self.items_inside.append(item)
	
	def __str__(self):
		str = "You are in the %s. %s \n" % (self.name, self.description)
		if len(self.items_inside) > 0:
			str += " You see: "
			for i in self.items_inside:
				str += i.__str__() + "\n "
		return str