import config

import decimal

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
				try:
					hRight = height[h+1]
				except:
					hRight = height[h]
				
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
		
	def difference(self, centre, other): # To decide which is the larger number, ONLY FOR USE WITH THE CENTRE
		def difference2(n1, n2): # Finds difference
			return (n1 - n2)
			
		if (centre < other): # Decides what is the biggest number, and calls difference2
			tileSize = difference2(centre, other)
			tileSize1 = decimal.Decimal(centre)-decimal.Decimal(other)
			tileSize2 = decimal.Decimal(tileSize1)/2
			self.CB += 1
			#print self.CB,self.CS
			return other + decimal.Decimal(tileSize2)
			
		elif (other < centre):
			tileSize = difference2(other, centre)
			tileSize1 = decimal.Decimal(other)-decimal.Decimal(centre)
			tileSize2 = decimal.Decimal(tileSize1)/2
			self.CS += 1
			#print self.CS,self.CB
			return centre + decimal.Decimal(tileSize2)
		else:
			return centre
			
	def otherDifference(self, MAC, LAC): # For the corners of tiles, Most Anti-Clockwise, Least Anti-Clockwise
		def difference2(n1, n2):
			return (n1 - n2)
		if (MAC < LAC):
			tileSize = difference2(MAC, LAC)
			biggest = MAC
			smallest = LAC
		elif (LAC < MAC):
			tileSize = difference2(LAC, MAC)
			biggest = LAC
			smallest = MAC
		else:
			return MAC
		tileSize1 = decimal.Decimal(biggest)-decimal.Decimal(smallest)
		tileSize2 = decimal.Decimal(tileSize1)/2
		tileSize3 = smallest + decimal.Decimal(tileSize2)
		return tileSize3

	def ifEdge(self, list, current, x):
		if (current < len(list)):
			def task(a, r):
				if a == r:
					return True
				else:
					return False
					
			self.edgeL = False
			self.edgeR = False
			
			actual = decimal.Decimal(current - 1)/x
			rounded = round(actual)
			
			if task(actual, rounded) == True:
				self.edgeL = True
				
			try:
				actual = decimal.Decimal(current + 1)/x
			except:
					actual = decimal.Decimal(current)/x
			
			rounded = round(actual)
			
			print str(current)+"  ",actual,rounded
			
			if task(actual, rounded) == True:
				self.edgeR = True
		
	def loadPoints(self, HC, x): # Starts bottom left, works round ANTIclockwise
		points = [] # A list containing a list of points for each square
		self.CB = 0
		self.CS = 0
		def loadDaPoints(listLoad): # Works out what each corner 
			squarePoints = [] # The points for each square
			centre = int(listLoad[0])
			above = int(listLoad[1])
			below = int(listLoad[2])
			left = int(listLoad[3])
			right = int(listLoad[4])
			
			try:
				previousTile = points[len(points)-1]
			except:
				previousTile = [centre, centre, centre, centre, centre, centre, centre]
				
			try:
				belowTile = points[len(points)-x]
			except:
				belowTile = [centre, centre, centre, centre, centre, centre, centre]
			#print centre, above, below, left, right
			
			bottomCentre = self.difference(centre, below)
			rightCentre = self.difference(centre, right)
			topCentre = self.difference(centre, above)
			leftCentre = self.difference(centre, left)
			bottomLeft = previousTile[3]
			#bottomLeft = self.otherDifference(leftCentre, bottomCentre)
			bottomRight = belowTile[5]
			topRight = self.otherDifference(rightCentre, topCentre)
			topLeft = previousTile[5]
			
			#topLeft = self.otherDifference(leftCentre, topCentre)
			
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
			#print squareData
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
