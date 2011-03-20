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
	
	# The following properties get filled when the tile types are loaded
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
		try:
			self.file = zipfile.ZipFile(filename, "r")
		except:
			raise IOError, "Couldn't load map file"
		try:
			mapinfo_string = self.file.read("map.cfg")
		except:
			raise IOError, "Couldn't read map.cfg"
		self.data_parser = ConfigParser.ConfigParser()
		self.data_parser.readfp(StringIO.StringIO(mapinfo_string))
		self.name = self.data_parser.get("map", "name")
		self.description = self.data_parser.get("map", "desc")
		old_type = self.data_parser.getboolean("map", "old_format")
		if old_type:
			self.generate_tile_array = self.generate_tile_array_old_format
		try:
			self.data_offset = self.data_parser.get("map", "map_data_offset")
		except:
			self.data_offset = 0
	def generate_tile_array(self):
		self.width = self.data_parser.getint("map", "width")
		self.height = self.data_parser.getint("map", "height")
		
		wall = self.file.open("maps/wall.map", "r")
		resource = self.file.open("maps/resource.map", "r")
		wall.read(self.data_offset)
		resource.read(self.data_offset)
		wallData = wall.read()
		resourceData = resource.read()
		if len(wallData) != (self.width*self.height*4):
			raise ValueError, "Wall file has bad length"
		if len(resourceData) != (self.width*self.height*4):
			raise ValueError, "Resource file has bad length"
		
		tiles = []
		for tilenum in range(self.width*self.height):
			wallValue = wallData[tilenum*4:(tilenum+1)*4:]
			resD = resourceData[tilenum*4:(tilenum+1)*4:]
			
			wallType = struct.unpack("<I", wallValue)[0]
			crystals, ore = struct.unpack("<HH", resD)
			x, y = tilenum%self.width, tilenum//self.width
			tiles.append(Tile(x, y, wallType, crystals, ore))

		return tiles

	def generate_tile_array_old_format(self):
		self.width = self.data_parser.getint("map", "width")
		self.height = self.data_parser.getint("map", "height")
		
		wall = self.file.open("maps/wall.map", "r")
		resource = self.file.open("maps/resource.map", "r")
		wall.read(self.data_offset)
		resource.read(self.data_offset)
		wallData = wall.read()
		resourceData = resource.read()
		if len(wallData) != (self.width*self.height*4) + 8:
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
