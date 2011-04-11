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
		
		self.texture = None
	def applyCharacteristics(self, target): # The loaded model?
		target.fullName = self.fullName # The name of the square
		target.model = self.model # The model of the square
		target.solid = self.solid # If the square is solid [drillable] (duh)
		target.canWalk = self.canWalk # If it can be walked on
		target.isWater = self.isWater # If it's water
		target.speedCoef = self.speedCoef # The 'bonus' of walking on the square
		target.drillTime = self.drillTime # Drill time of the square
		target.conductPower = self.conductPower # If the square is a power path
		target.texture = self.texture
		print target.texture
		
class WorldLoader:
	def __init__(self, height, x):
		self.drawStuff(height, x)
	
	def drawStuff(self, height, x):
		heightCoords = []
		h = 0
		while(h < len(height)):
			height2 = [] # Centre, above, below, left, right
			self.ifEdge(height, h, x)
			hCentre = height[h]
			if self.edgeL == True:
				hLeft = height[h]
			else:
				hLeft = height[h-1]
			if self.edgeR == True:
				hRight = height[h]
			else:
				hLeft = height[h+1]
			try:
				hAbove = height[h+x]
			except:
				hAbove = height[h]
			try:
				hBelow = height[h-x]
			except:
				hBelow = height[h]
				
			height2.append(hCentre)
			height2.append(hAbove)
			height2.append(hBelow)
			height2.append(hLeft)
			height2.append(hRight)
			heightCoords.append(height2)
			h += 1
			
		# print heightCoords
		points = self.loadPoints(heightCoords, x)
		return points

	def ifEdge(self, list, current, x):
		def task(a, r):
			if a == r:
				return True
			else:
				return False
		self.edgeL = False
		self.edgeR = False
		
		actual = (current - 1)/x
		rounded = round(actual)
		
		if task(actual, rounded) == True:
			self.edgeL = True
			
		actual = (current + 1)/x
		rounded = round(actual)
		
		if task(actual, rounded) == True:
			self.edgeR = True
		
	def loadPoints(self, HC, x): # Starts bottom left, works round ANTIclockwise
		points = [] # A list containing a list of points for each square
		def loadDaPoints(listLoad): # Works out what each corner 
			squarePoints = [] # The points for each square
			centre = int(listLoad[0])
			above = int(listLoad[1])
			below = int(listLoad[2])
			left = int(listLoad[3])
			right = int(listLoad[4])
			#print centre, above, below, left, right
			
			bottomLeft = centre - (left - below)/2
			bottomCentre = centre - (centre - below)/2
			bottomRight = centre - (right - below)/2
			rightCentre = centre - (centre - right)/2
			topRight = centre - (right - above)/2
			topCentre = centre - (centre - above)/2
			topLeft = centre - (above - left)/2
			leftCentre = centre - (left - centre)/2
			
			squarePoints.append(centre)
			squarePoints.append(bottomLeft)
			squarePoints.append(bottomCentre)
			squarePoints.append(bottomRight)
			squarePoints.append(rightCentre)
			squarePoints.append(topRight)
			squarePoints.append(topCentre)
			squarePoints.append(topLeft)
			squarePoints.append(leftCentre)
			points.append(squarePoints)
			
		tempNo = 0
		while(tempNo < len(HC)):
			squareData = HC[tempNo] # Gets the square info from the grid (see drawStuff)
			loadDaPoints(squareData)
			tempNo+=1
			
		return points
			
	
	
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
	theType.texture = wallConfig.get(tname, "texture")
	if not theType.solid: # things that only apply if the wall isn't solid
		theType.canWalk = wallConfig.getboolean(tname, "walkable")
		theType.isWater = wallConfig.getboolean(tname, "water")
		theType.speedCoef = wallConfig.getfloat(tname, "speed_coef")
	else:
		theType.drillTime = wallConfig.getfloat(tname, "drillTime") # only solid walls can be drilled
	theType.conductPower = wallConfig.getboolean(tname, "conductor") # power path
	wallTypes[iT] = theType
