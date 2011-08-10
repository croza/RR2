import ConfigParser
import StringIO # For reading map files

import binascii # For dealing with the hex of the .map files
import copy

class mapLoader:
	def __init__(self, ParserClass):
		self.mapDir = ParserClass.main['main']['testing_map']
		try:
			self.mapConfigFile = open(self.mapDir + "map.cfg")
		except:
			raise IOError, "Couldn't open the map config file"
			
		try:
			self.mapConfigFileData = self.mapConfigFile.read()
		except:
			raise IOError, "Couldn't read the map config file"
			
		self.mapConfigParser = ConfigParser.ConfigParser() # To parse the map config file
#		self.mapConfigParser.readfp(StringIO.StringIO(self.mapConfigFileData))
		self.mapConfigParser.read(self.mapDir + "map.cfg")
		
#		name = self.mapConfigParser.get("map", "name")
#		description = self.mapConfigParser.get("map", "desc")
		
		self.tileArray = self.ganerate_tile_array(ParserClass)
		
		print 'END OF MAPLOADER.PY!'
		
	def ganerate_tile_array(self, ParserClass):
		self.width = self.mapConfigParser.getint("map", "width") # Width of the map	(from the config)
		self.height = self.mapConfigParser.getint("map", "height") # Height of the map
		
		mapFiles = [] # A list, containg the data of the map files
		
		surf = open(self.mapDir+"maps/Surf.map", "r")
		high = open(self.mapDir+"maps/High.map", "r")
		reda = open(self.mapDir+"maps/Reda.map", "r")
		renu = open(self.mapDir+"maps/Renu.map", "r")

		wallData = surf.read() # Turning the map file into a string
		mapFiles.append(wallData)
		highData = high.read()
		mapFiles.append(highData)
		redaData = reda.read()
		mapFiles.append(redaData)
		renuData = renu.read()
		mapFiles.append(renuData)
		
		for mapFile in mapFiles:
			if (len(mapFile) != (self.width*self.height)):
				raise ValueError, "%s file has bad length" % (mapFile)
				
		tiles = [] # A list of rows
		row = [] # The data of each row
		
		Xpos = 0 # The square currently on
		Ypos = 0
		
		for tilenum in range(self.width * self.height):
			print tilenum
			tilenum = tilenum +1 # Helps with maths (can't remeber how, but it does)
			
			wallStr = binascii.hexlify(wallData[tilenum-1]) # Converts the hex into a two character sting
			wallInt = int('0x'+wallStr, 0) # Converts the string to an integer
			
			highStr = binascii.hexlify(highData[tilenum-1]) # Same, but for the High.map file
			highInt = int('0x'+highStr, 0)
			
			redaStr = binascii.hexlify(redaData[tilenum-1])
			redaInt = int('0x'+redaStr, 0)
			
			renuStr = binascii.hexlify(renuData[tilenum-1])
			renuInt = int('0x'+renuStr, 0)
			
			if (tilenum == 0): # For only the first tile of the map (because otherwise everything is 1 char long)
				tempClass = copy.copy(ParserClass.wall[ParserClass.main['wall_types'][wallInt]])
				tempClass.posZ = highInt
				tempClass.reda = redaInt
				tempClass.renu = renuInt
				
				row.append(tempClass)
				tilenum += 1
				
			elif (tilenum % self.width != 0): # If it is not the end of the row
				tempClass = copy.copy(ParserClass.wall[ParserClass.main['wall_types'][wallInt]])
				tempClass.posZ = highInt
				tempClass.reda = redaInt
				tempClass.renu = renuInt
				
				row.append(tempClass)
				tilenum += 1
				
			elif (Xpos % self.width == 0): # If it is the end of the row
				tempClass = copy.copy(ParserClass.wall[ParserClass.main['wall_types'][wallInt]])
				tempClass.posZ = highInt
				tempClass.reda = redaInt
				tempClass.renu = renuInt
				
				row.append(tempClass)
				tiles.append(row)
				row = []
				
		return tiles