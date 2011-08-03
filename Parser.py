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
				else:
					return number
				
		self.main = {}
		self.user = {}
		self.wall = {}
		self.unit = {}
		
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
			
		print self.main
		print self.user
		print self.wall
		print self.unit
		print 'END OF PARSER.PY!'
		
class wallClasses: # Makes a class out of a dict
	def __init__(self, dictionary):#, name):
#		self.name = name
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
		
class unitClasses:
	def __init__(self, dictionary):#, name):
#		self.name = name
		self.fullName = dictionary['fullname']
		self.HP = dictionary['hp']
		self.info = dictionary['info']
		self.model = dictionary['model']
		self.radius = dictionary['radius']
		self.mass = dictionary['mass']
		self.startforce = dictionary['startforce']
		self.maxforce = dictionary['maxforce']
		self.digmulti = dictionary['digmulti']
		self.reinforcemulti = dictionary['reinforcemulti']
		self.shovelmulti = dictionary['shovelmulti']
			
#p = Parser()