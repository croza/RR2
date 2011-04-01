import config

class WallType:
	def __init__(self):
		# Adding names to allow their later filling by the config reader
		self.fullName = None
		self.modelName = None
		
		#Properties that affect moving over the tile
		self.solid = None
		self.canWalk = None
		self.isWater = None
		self.speedCoef = None
		
		self.drillTime = None
		self.conductPower = None
	def applyCharacteristics(self, target): # The loaded model?
		target.fullName = self.fullName # The name of the square
		target.model = self.model # The model of the square
		target.solid = self.solid # If the square is solid [drillable] (duh)
		target.canWalk = self.canWalk # If it can be walked on
		target.isWater = self.isWater # If it's water
		target.speedCoef = self.speedCoef # The 'bonus' of walking on the square
		target.drillTime = self.drillTime # Drill time of the square
		target.conductPower = self.conductPower # If the square is a power path

wallCfgFile = config.parser.getpath("main", "wall_config_file") # Get whatever config file is running (pre cut up)?
wallConfig = config.RRcfgParser() # 
wallConfig.read(wallCfgFile)
wallTypes = {} # the different types of wall in integer form (0, 1, 2 etc.)
wallTypeNums = config.parser.options("wall_types")
for t in wallTypeNums:
	tname = config.parser.get("wall_types", t) # tname = internal wall type name
	try:
		iT = int(t)
	except:
		raise config.ConfigError, "Non-integer wall type: %s" % t
	theType = WallType()
	theType.fullName = wallConfig.get(tname, "fullName")
	theType.model = wallConfig.getpath(tname, "model") # The path to the wall file models?
	theType.solid = wallConfig.getboolean(tname, "solid")
	if not theType.solid: # things that only apply if the wall isn't solid
		theType.canWalk = wallConfig.getboolean(tname, "walkable")
		theType.isWater = wallConfig.getboolean(tname, "water")
		theType.speedCoef = wallConfig.getfloat(tname, "speed_coef")
	else:
		theType.drillTime = wallConfig.getfloat(tname, "drillTime") # only solid walls can be drilled
	theType.conductPower = wallConfig.getboolean(tname, "conductor") # power path
	wallTypes[iT] = theType
