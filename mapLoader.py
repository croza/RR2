import ConfigParser
import StringIO

import binascii
import copy

class mapLoader:
	def __init__(self, mapDir):
		self.mapDir = mapDir

		try:
			mapinfo_string_2 = open(self.mapDir+"map.cfg") # If the map file can be read
		except:
			raise IOError, "Couldn't open map.cfg"
			
		try:
			mapinfo_string = mapinfo_string_2.read() # If the map file can be read
		except:
			raise IOError, "Couldn't read map.cfg"
			
		self.data_parser = ConfigParser.ConfigParser() # A config parser to read the internal map configs
		self.data_parser.readfp(StringIO.StringIO(mapinfo_string))
		self.name = self.data_parser.get("map", "name") # Map name
		self.description = self.data_parser.get("map", "desc") # The description of the map
		
		print 'END OF MAPLOADER!'
		
		## ALL MAPS ARE THE NEWEST FORMAT; to get to this format use the map converter (in tools) to convert maps made by Cyrem's map creator.
			
	def generate_tile_array(self, Parser): # The parser bit represent a dictionary containing the classes for the wall types
		self.width = self.data_parser.getint("map", "width") # Width of the map	(from the config)
		self.height = self.data_parser.getint("map", "height") # Height of the map
		
		mapFiles = []
		
		surf = open(self.mapDir+"maps/Surf.map", "r")
		high = open(self.mapDir+"maps/High.map", "r")

		wallData = surf.read() # Turning the map file into a string
		mapFiles.append(wallData)
		highData = high.read()
		mapFiles.append(highData)
		# print wall.read()
		
		for mapFile in mapFiles:
			if (len(mapFile) != (self.width*self.height)):
				print len(mapFile), self.mapDir+"maps/%s" % (mapFile)
				raise ValueError, "%s file has bad length" % (mapFile)

		tiles = [] # A list of rows
		row = [] # The data of each row
		
		Xpos = 0 # The square currently on
		Ypos = 0
		
		for tilenum in range(self.width*self.height): # For tilenum in range <size of map>. Makes a class for each square (see config) and puts this into a row, then that row into a larger list of rows.
			tilenum = tilenum+1 # Helps with maths (can't remeber how, but it does)
			x, y = tilenum%self.width, tilenum//self.width
			
			wallStr = binascii.hexlify(wallData[tilenum-1]) # Converts the hex into a two character sting
			wallInt = int('0x'+wallStr, 0) # Converts the string to an integer
			
			highStr = binascii.hexlify(highData[tilenum-1])
			highInt = int('0x'+highStr, 0)
			
			if (tilenum == 0): # For only the first tile of the map (because otherwise everything is 1 char long)
				tempClass = copy.copy(Parser.classes[wallInt])
				tempClass.posZ = highInt
				
				row.append(tempClass)
				tilenum += 1
				
			elif (tilenum % self.width != 0): # If it ia not the end of the row
				tempClass = copy.copy(Parser.classes[wallInt])
				tempClass.posZ = highInt
				
				row.append(tempClass)
				tilenum += 1
				
			elif (Xpos % self.width == 0): # If it is the end of the row
				tempClass = copy.copy(Parser.classes[wallInt])
				tempClass.posZ = highInt
				
				row.append(tempClass)
				tiles.append(row)
				row = []
				
			
		return tiles # Returns a list with all the wall data in