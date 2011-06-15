import ConfigParser
import StringIO

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
		
		#self.DATA = self.generate_tile_array()
		
		## ALL MAPS ARE THE NEWEST FORMAT; to get to this format use the map converter (in tools) to convert maps made by Cyrem's map creator.
			
	def generate_tile_array(self, Parser): # Makes an array for the grid?
		self.width = self.data_parser.getint("map", "width") # width of the map	(from the config)
		self.height = self.data_parser.getint("map", "height") # Height of the map
		wall = open(self.mapDir+"maps/Surf.map", "r")

		wallData = wall.read() # Turning the map file into a string
		print wall.read()

		if len(wallData) != (self.width*self.height):		# If the length of the array is not equal to height * width, raise error
			print len(wallData), self.mapDir+"maps/Surf.map"
			raise ValueError, "Surf file has bad length"

		tiles = [] # A list of rows
		row = [] # The data of each row
		
		Xpos = 0 # The square currently on
		Ypos = 0
		
		for tilenum in range(self.width*self.height): # For tilenum in range <size of map>. Makes a class for each square (see config) and puts this into a row, then that row into a larger list of rows.
			tilenum = tilenum+1 # Helps with maths (can't remeber how, but it does)
			x, y = tilenum%self.width, tilenum//self.width
			wallInt = wallData[tilenum-1]
			#print 'hi', tilenum, wallInt
			
			if (tilenum == 0): # For only the first tile of the map (because otherwise everything is 1 char long)
				row.append(Parser.classes[int(wallInt)])
				tilenum += 1
				
			elif (tilenum % self.width != 0): # If it ia not the end of the row
				row.append(Parser.classes[int(wallInt)])
				tilenum += 1
				
			elif (Xpos % self.width == 0): # If it is the end of the row
				row.append(Parser.classes[int(wallInt)])
				tiles.append(row)
				print len(row)
				row = []
			
		return tiles # Returns a list with all the wall data in