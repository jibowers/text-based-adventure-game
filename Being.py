
class Being:

	## can be either monster or human (you)
	def __init__(self, id, name, description, attacks):
		self.id = id
		self.name = name
		self.description = description
		self.attacks = attacks ##list of attacks
		self.health_points = 100
		self.willingness = 100
		
class Monster(Being):

	def __init__(self, id, name, description, attacks):
		super(Monster, self).__init__(id, name, description, attacks)
		self.been_beaten = False

	## baby I'm not a monster
	
"""
class Human(Being): ## aka user
	def __init__(self, id, name, description, attacks):
		super(Human, self).__init__(id, name, description, attacks)
"""