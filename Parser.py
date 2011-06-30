import ConfigParser

class config:
	def __init__(self):
		self.mainConfig = ConfigParser.ConfigParser() # The config for the main.cfg file
		self.mainConfig.read("./data/config/main.cfg")
		self.mapFile = self.mainConfig.get("main", "testing_map")
		
		self.wallConfig = ConfigParser.ConfigParser() # The config for the wall.cfg file
		self.wallConfig.read(self.mainConfig.get('main', 'wall_config_file'))
		
		self.unitConfig = ConfigParser.ConfigParser()
		self.unitConfig.read(self.mainConfig.get('main', 'unit_config_file'))
		
		# For the next bit, it deals with the wall types, and  other things that only have to be run once.
		
#		self.details = {} # The details of each wall type
#		classes = [] # A list of wall clases, to be put into a dictionary of all classes
		
		self.classes = {} # NEWSEST DICT OF CLASSES
		
		self.units = {}
		
		wallList = [] # A listof all the options within the wall secion, used to order the sections numerically
		
		wallSections = self.wallConfig.sections()
		section2 = 0
		
		for option in self.mainConfig.options('wall_types'): # for each option in wall_types in the main.cfg
			self.classes[int(option)] = wallClasses(self.loadWalls(self.wallConfig.items(self.mainConfig.get('wall_types', option))), self.mainConfig.get('wall_types', option)) # Makes a class for each wall type, and puts them into a list with the corresponding number

		for option in self.mainConfig.options('units'):
			self.units[int(option)] = unitClasses(self.loadWalls(self.unitConfig.items(self.mainConfig.get('units', option))), self.mainConfig.get('units', option))
			
		# print self.classes # The long dictionary before the end of parser bit (below)
		print 'END OF PARSER!'
		
	def loadWalls(self, list1): # Takes the data from the config, and turns it into a useful dictionary, which is then converted into a class (see wallClasses)
		def isNumber(number): # Run for all, test to see if it is a number, and returns a float if it is
			try:
				float(number)
				return True
			except ValueError:
				return False
				
		sectionData = {} # Where all the data for the section should end up
		
		for lineData in list1: # Line data is sort of like one line in each section. It's in a tuple, so has to be converted to a list...
			data = list(lineData) # ...as done here
			
			if (data[1].capitalize() == 'Yes'): # Testing to see if it's a boolean (must be a better way, but meh)
				data[1] = True
			elif (data[1].capitalize() == 'No'):
				data[1] = False
			elif (isNumber(data[1]) == True): # Checking to see if it's a number
				data[1] = float(data[1])
			elif (data[1].capitalize() == 'None'):
				data[1] = None
			else:
				pass # Should already be a string, so nothing to do here
				
			sectionData[data[0]] = data[1]
		
		return sectionData
		
#	def loadUnits(self, unitList):
#		unitData = {}
#		for lineData in unitList:
#			data = list(lineData) # Converts the tuple to a list
			
		
class wallClasses: # Makes a class out of a dict
	def __init__(self, dictionary, name):
		self.name = name
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
	def __init__(self, dictionary, name):
		self.name = name
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
		