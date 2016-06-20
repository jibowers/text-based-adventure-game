
class Attack:
	def __init__(self, id, name, description, uses, power, compassion):
		self.id = id
		self.name = name
		self.description = description
		self.power = power # int between 0-100  KILLING POWER
		self.compassion = compassion ## POWER TO LOWER WILLINGNESS
		self.uses = uses #int
