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
		
		self.loadConfigs()
		
	def loadConfigs(self):
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

		print 'END OF PARSER.PY!'
		
class wallClasses: # Makes a class out of a dict
	def __init__(self, dictionary):#, name):
		self.conductor = dictionary['conductor']
		self.fullName = dictionary['fullname']
		self.walkable = dictionary['walkable']
		self.water = dictionary['water']
		self.lava = dictionary['lava']
		self.solid = dictionary['solid']
		self.speed_coef = dictionary['speed_coef']
		self.drillTime = dictionary['drilltime']
		self.conductor = dictionary['conductor']
		self.texture = dictionary['texture']
		self.selectable = dictionary['select']
		self.dynamite = dictionary['dynamite']
		self.reinforce = dictionary['reinforce']
		
class unitClasses:
	def __init__(self, dictionary):#, name):
		self.fullName = dictionary['fullname']
		self.HP = dictionary['hp']
		self.info = dictionary['info']
		self.moveType = dictionary['movetype']
		self.model = dictionary['model']
		self.radius = dictionary['radius']
		self.mass = dictionary['mass']
		self.startForce = dictionary['startforce']
		self.maxForce = dictionary['maxforce']
		self.digMulti = dictionary['digmulti']
		self.reinforceMulti = dictionary['reinforcemulti']
		self.shovelMulti = dictionary['shovelmulti']
		
class objectClasses:
	def __init__(self, dictionary):
		self.pickup = dictionary['pickup']
		self.eValue = dictionary['evalue']
		self.oValue = dictionary['ovalue']
		self.stableTime = dictionary['stabletime']
		self.charge = dictionary['charge']
		self.decharge = dictionary['decharge']
#pickup: yes
#evalue: 0
#ovalue: 0
#stabletime: none
#charge: energy_crystal
#decharge: none