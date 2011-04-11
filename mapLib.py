import zipfile
import StringIO
import ConfigParser
import struct
import wallTypes

class Tile:
	def __init__(self, x, y, t, ec, ore):
		self.x = x
		self.y = y
		self.typeInt = t
		self.cry = ec
		self.ore = ore
	def __repr__(self):
		return "<Tile at %i, %i, type %s, %i ore and %i crystals>" % (self.x, self.y, self.typeInt, self.ore, self.cry)
	def toData(self):
		wall = struct.pack("<I", self.typeInt)
		resource = struct.pack("<HH", self.ore, self.cry)
		return wall, resource
	
	# The following properties get filled when the tile types are loaded **'STORAGE' values**
	fullName = None
	modelName = None
	solid = None
	canWalk = None
	isWater = None
	speedCoef = None
	drillTime = None
	conductPower = None
	
	model = None
		

class Map:
	def __init__(self, filename):
		print filename
		try:
			self.file = zipfile.ZipFile(filename, "r") #If the map (in a .zip) exists:
		except:
			raise IOError, "Couldn't load map file"
		try:
			mapinfo_string = self.file.read("map.cfg") # If the map file can be read
		except:
			raise IOError, "Couldn't read map.cfg"
		self.data_parser = ConfigParser.ConfigParser() # ?????
		self.data_parser.readfp(StringIO.StringIO(mapinfo_string))
		self.name = self.data_parser.get("map", "name") # Map name
		self.description = self.data_parser.get("map", "desc") # The description of the map
		old_type = self.data_parser.getboolean("map", "old_format") # If the map is of the 'old' RR format (bool)
		if old_type:
			self.generate_tile_array = self.generate_tile_array_old_format # Stuff to do if the map is of the 'old' format
		try:
			self.data_offset = self.data_parser.get("map", "map_data_offset")
		except:
			self.data_offset = 0
			
	def generate_tile_array(self): # Makes an array for the grid?
		self.width = self.data_parser.getint("map", "width") # width of the map	
		self.height = self.data_parser.getint("map", "height") # Height of the map
		wall = self.file.open("maps/wall.map", "r")
		resource = self.file.open("maps/resource.map", "r")
		wall.read(self.data_offset)
		resource.read(self.data_offset)
		wallData = wall.read() # Turning the map file into a string
		resourceData = resource.read()
		if len(wallData) != (self.width*self.height*4): # If the length of the array is not equal to height * width, raise error
			raise ValueError, "Wall file has bad length"
		if len(resourceData) != (self.width*self.height*4): # If the length of the file is not equal...
			raise ValueError, "Resource file has bad length"
		tiles = []
		
		for tilenum in range(self.width*self.height): # For tilenum in range <size of map>
			wallValue = wallData[tilenum*4:(tilenum+1)*4:] # The un-hex'd value of the wall file
			resD = resourceData[tilenum*4:(tilenum+1)*4:] # Same with the resource file
			
			wallType = struct.unpack("<I", wallValue)[0] # Converting the wall type into an int (found it :D)
			crystals, ore = struct.unpack("<HH", resD)
			x, y = tilenum%self.width, tilenum//self.width
			tiles.append(Tile(x, y, wallType, crystals, ore))
			
		return tiles # Returns a list with all the wall data in
		
	def getHeightMap(self):
		self.width = self.data_parser.getint("map", "width") # width of the map	
		self.height = self.data_parser.getint("map", "height") # Height of the map
		height = self.file.open("maps/height.map") # For the height
		height.read(self.data_offset)
		heightData = height.read()
		heightMap = []
		for h in range(self.width*self.height):
			heightValue = heightData[h*4:(h+1)*4:]
			heightV = struct.unpack("<I", heightValue)[0]
			heightMap.append(heightV)
			
		return heightMap
		
	def generate_tile_array_old_format(self):
		self.width = self.data_parser.getint("map", "width")
		self.height = self.data_parser.getint("map", "height")
		
		wall = self.file.open("maps/wall.map", "r") # The wall map file
		resource = self.file.open("maps/resource.map", "r") # The resource map file
		wall.read(self.data_offset)
		resource.read(self.data_offset)
		wallData = wall.read() # Reading...
		resourceData = resource.read() # Reading...
		if len(wallData) != (self.width*self.height*4) + 8: # Explanitary, really
			raise ValueError, "Wall file has bad length"
		if len(resourceData) != (self.width*self.height*4) + 8:
			raise ValueError, "Resource file has bad length"
		
		tiles = []
		for tilenum in range(self.width*self.height):
			wallValue = wallData[tilenum*4:(tilenum+1)*4:]
			resD = resourceData[tilenum*4:(tilenum+1)*4:].encode("hex") # [str].encode("hex") converts "\x01" to 01 etc
			
			wallType = struct.unpack("<I", wallValue)[0]
			crystals = ore = 0 # TODO: Properly read Cror data
			x, y = tilenum%self.width, tilenum//self.width
			tiles.append(Tile(x, y, wallType, crystals, ore))

		return tiles

if __name__ == "__main__":
	print "\n".join([str(tile) for tile in Map("sample_map.zip").generate_tile_array()])
	t = Tile(0, 0, 1, 0, 1)
	print t, "=>", t.toData()
