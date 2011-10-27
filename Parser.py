import ConfigParser

class Parser:
	def __init__(self):
		self.mainConfig = ConfigParser.ConfigParser()
		self.mainConfig.read("./data/config/main.cfg")
		
		self.userConfig = ConfigParser.ConfigParser()
		self.userConfig.read(self.mainConfig.get('main', 'user_config_file'))
		
		self.wallConfig = ConfigParser.ConfigParser()
		self.wallConfig.read(self.mainConfig.get('main', 'wall_config_file'))
		
		self.unitConfig = ConfigParser.ConfigParser()
		self.unitConfig.read(self.mainConfig.get('main', 'unit_config_file'))
		
		self.objectConfig = ConfigParser.ConfigParser()
		self.objectConfig.read(self.mainConfig.get('main', 'object_config_file'))
		
		self.buildingConfig = ConfigParser.ConfigParser()
		self.buildingConfig.read(self.mainConfig.get('main', 'building_config_file'))
		
#		self.loadConfigs()
		
#	def loadConfigs(self):
		def isNumber(number): # Run for all, test to see if it is a number, and returns a float if it is
			try:
				float(number)
				if (float(number) == int(number)):
					return int(number)
				else:
					return float(number)
			except ValueError:
				if (number.capitalize() == 'Yes'):
					return True
				elif (number.capitalize() == 'No'):
					return False
				elif (number.capitalize() == 'None'):
					return None
				else:
					return number
				
		self.main = {}
		self.user = {}
		self.wall = {}
		self.unit = {}
		self.object = {}
		self.building = {}
		
		for section in self.mainConfig.sections():
			data = {}
			for option in self.mainConfig.options(section):
				data[isNumber(option)] = isNumber(self.mainConfig.get(section, option))
			self.main[section] = data
			
		for section in self.userConfig.sections():
			data = {}
			for option in self.userConfig.options(section):
				data[isNumber(option)] = isNumber(self.userConfig.get(section, option))
			self.user[section] = data
			
		for section in self.wallConfig.sections():
			data = {}
			for option in self.wallConfig.options(section):
				data[isNumber(option)] = isNumber(self.wallConfig.get(section, option))
			self.wall[section] = wallClasses(data)
			
		for section in self.unitConfig.sections():
			data = {}
			for option in self.unitConfig.options(section):
				data[isNumber(option)] = isNumber(self.unitConfig.get(section, option))
			self.unit[section] = unitClasses(data)
			
		for section in self.objectConfig.sections():
			data = {}
			for option in self.objectConfig.options(section):
				data[isNumber(option)] = isNumber(self.objectConfig.get(section, option))
			self.object[section] = objectClasses(data)
		
		for section in self.buildingConfig.sections():
			data = {}
			for option in self.buildingConfig.options(section):
				data[isNumber(option)] = isNumber(self.buildingConfig.get(section, option))
			self.building[section] = buildingClasses(data)
		
		
		print self.building
		print 'END OF PARSER.PY!'
		
class wallClasses: # Makes a class out of a dict
	def __init__(self, dictionary):#, name):
		self.conductor = dictionary['conductor'] # Whether it conducts (power walls?)
		self.fullName = dictionary['fullname'] # The name (GUI stuff)
		self.walkable = dictionary['walkable'] # Whether it can be walked on
		self.water = dictionary['water'] # Whether it's water (for water untis)
		self.lava = dictionary['lava'] # Whether it's lava (flying)
		self.solid = dictionary['solid'] # Whwther it can be passed through
		self.speed_coef = dictionary['speed_coef'] # How fast units move through it
		self.drillTime = dictionary['drilltime'] # How quickly it drills (100hp per second at 1x drilling)
		self.texture = dictionary['texture'] # The texture file of the wall
		self.selectable = dictionary['select'] # Whether the wall can be selected
		self.dynamite = dictionary['dynamite'] # Can it be dynamited?
		self.reinforce = dictionary['reinforce'] # Can it be reinforced?
		
class unitClasses:
	def __init__(self, dictionary):#, name):
		self.fullName = dictionary['fullname'] # The name for the GUI
		self.HP = dictionary['hp'] # The HP
		self.info = dictionary['info'] # Any info about the unit
		self.moveType = dictionary['movetype'] # Air, land or water
		self.model = dictionary['model'] # The path to the model
		self.radius = dictionary['radius'] # The bounding radius of the object (used for drilling etc.)
		self.mass = dictionary['mass'] # The mass
		self.startForce = dictionary['startforce'] # The force that the unit starts moving at
		self.maxForce = dictionary['maxforce'] # The maximum move force
		self.dig = dictionary['digmulti'] # How quickly it drills
		self.reinforce = dictionary['reinforcemulti'] # How quickly it reinforces
		self.shovel = dictionary['shovelmulti'] # How quickly it shovels
		self.hold = dictionary['hold'] # How many items it can hold
		self.modelHeight = dictionary['modelheight'] # The maximum height of the model
		self.selectScale = dictionary['selectscale'] # How big the select... thing... should be
		self.job = False
		
class objectClasses:
	def __init__(self, dictionary):
		self.model = dictionary['model'] # The path to the model
		self.pickup = dictionary['pickup'] # How many slots (hold) it will take up
		self.eValue = dictionary['evalue'] # The energy crystal value of the item
		self.oValue = dictionary['ovalue'] # The ore value of the item
		self.stableTime = dictionary['stabletime'] # How long before it decharges
		self.charge = dictionary['charge'] # What it charges up into
		self.decharge = dictionary['decharge'] # What it decharges into

class buildingClasses:
	def __init__(self, dictionary):
		self.HP = dictionary['hp']
		self.eCrystal = dictionary['ecrystal']
		self.ore = dictionary['ore']
		self.dynamite = dictionary['dynamite']
		self.model = dictionary['model']
		self.efence = dictionary['efence']