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
	def applyCharacteristics(self, target):
		target.fullName = self.fullName
		target.model = self.model
		target.solid = self.solid
		target.canWalk = self.canWalk
		target.isWater = self.isWater
		target.speedCoef = self.speedCoef
		target.drillTime = self.drillTime
		target.conductPower = self.conductPower

wallCfgFile = config.parser.getpath("main", "wall_config_file")
wallConfig = config.RRcfgParser()
wallConfig.read(wallCfgFile)
wallTypes = {}
wallTypeNums = config.parser.options("wall_types")
for t in wallTypeNums:
	tname = config.parser.get("wall_types", t) # tname = internal wall type name
	try:
		iT = int(t)
	except:
		raise config.ConfigError, "Non-integer wall type: %s" % t
	theType = WallType()
	theType.fullName = wallConfig.get(tname, "fullName")
	theType.model = wallConfig.getpath(tname, "model")
	theType.solid = wallConfig.getboolean(tname, "solid")
	if not theType.solid: # things that only apply if the wall isn't solid
		theType.canWalk = wallConfig.getboolean(tname, "walkable")
		theType.isWater = wallConfig.getboolean(tname, "water")
		theType.speedCoef = wallConfig.getfloat(tname, "speed_coef")
	else:
		theType.drillTime = wallConfig.getfloat(tname, "drillTime") # only solid walls can be drilled
	theType.conductPower = wallConfig.getboolean(tname, "conductor") # power path
	wallTypes[iT] = theType
