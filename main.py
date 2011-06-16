from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import VBase4, VBase3, GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, GeomNode, NodePath, Geom, AmbientLight, DirectionalLight
import direct.directbase.DirectStart

class world(DirectObject):
<<<<<<< HEAD
	def __init__(self, mapData):
		#print mapData
		
		models = []
		
		tileX = 0
		tileY = 0
		
		for row in mapData:
			print len(row)
			print row
			for tile in row:
				print dir(tile)
				#model = tile.model
				#tile.model.setPos(tile.posX, tile.posY, 0)
				#tile.model.reparentTo(render)
				#tex=loader.loadTexture(tile.texture)
				#print tex
				#tile.model.setTexture(tex, 1)
				#models.append(tile.model)
				#print tile.name, tile.posX, tile.posY, 0
=======
	def __init__(self, filename):
		self.map = mapLib.Map(filename)
		self.loadWorld()
		self.loadLight()
		
		s = moving2.HeightMoving(self.tiles)
		
	def loadWorld(self):
		self.tiles = []
		self.solidMap = []
		heightMap = self.map.getHeightMap()
		
		mapsize = self.map.getMapWidth() # The width of the map
		
		w = wallTypes.WorldLoader(heightMap, mapsize).drawStuff(heightMap, mapsize) # Gets the height for the points of each square
		ttiles = self.map.generate_tile_array() # The 'data' of all the squares in an array
		tileNumber = 0
		tex = loader.loadTexture('data/models/world/textures/ground.png')
		
		for tile in ttiles:
			# print tile
			wallTypes.wallTypes[tile.typeInt].applyCharacteristics(tile)
		
		for tile in ttiles:		
			aroundInfo = [] # The stuff below is to get the data for squares around the current square...
			try:
				above = ttiles[tileNumber+mapsize]
			except:
				above = ttiles[tileNumber]
			try:
				below = ttiles[tileNumber-mapsize]
			except:
				below = ttiles[tileNumber]
			try:
				right = ttiles[tileNumber+1]
			except:
				right = ttiles[tileNumber]
			try:
				left = ttiles[tileNumber-1]
			except:
				left = ttiles[tileNumber]
			try:
				belowLeft = ttiles[tileNumber-mapsize-1]
			except:
				belowLeft = ttiles[tileNumber]
			try:
				belowRight = ttiles[tileNumber-mapsize+1]
			except:
				belowRight = ttiles[tileNumber]
			try:
				aboveRight = ttiles[tileNumber+mapsize+1]
			except:
				aboveRight = ttiles[tileNumber]
			try:
				aboveLeft = ttiles[tileNumber+mapsize-1]
			except:
				aboveLeft = ttiles[tileNumber]
				
			#print tileNumber, tile.solid#, ttiles[tileNumber], left.solid
			if(tile.solid == True):
				if(above.solid == True): # 0 Starts above, goes round anti-clockwise, could def something for this...
					aroundInfo.append(1)
				else:
					aroundInfo.append(0)
					
				if(left.solid == True): # 1
					aroundInfo.append(1)
				else:
					aroundInfo.append(0)
					
				if(below.solid == True): # 2
					aroundInfo.append(1)
				else:
					aroundInfo.append(0)
					
				if(right.solid == True): # 3 ## Here and up are the tiles directly touching the current tile, below are the diagnal tiles
					aroundInfo.append(1)
				else:
					aroundInfo.append(0)
					
				if(belowLeft.solid == True): # 4
					aroundInfo.append(1)
				else:
					aroundInfo.append(0)
					
				if(belowRight.solid == True): # 5
					aroundInfo.append(1)
				else:
					aroundInfo.append(0)
					
				if(aboveRight.solid == True): # 6
					aroundInfo.append(1)
				else:
					aroundInfo.append(0)
					
				if(aboveLeft.solid == True): # 7
					aroundInfo.append(1)
				else:
					aroundInfo.append(0)
					
				# print aroundInfo
				
			else:
				aroundInfo = [0,0,0,0]
				# print aroundInfo
				
				
			tile.model = self.loadTriangles(w, tileNumber, tile, aroundInfo)
			tile.model.setCollideMask(0x1)
			tile.model.setPos((4*tile.x)-1, (4*tile.y)-1, 0)
			tile.model.reparentTo(render)

			tile.model.setTexture(loader.loadTexture(tile.texture), 1)
			self.tiles.append(tile)
			tileNumber += 1
			
		# print self.tiles
		
	def loadTriangles(self, list, number, tile, around):
		format = GeomVertexFormat.getV3n3c4t2()
		data = GeomVertexData("Data", format, Geom.UHStatic) 
		
		vertices = GeomVertexWriter(data, "vertex") # Vertices for just a plane tile
		texcoord= GeomVertexWriter(data, 'texcoord')
		
		vertices2 = GeomVertexWriter(data, "vertex") # Vertices for Junk (atm)
		texcoord2 = GeomVertexWriter(data, 'texcoord')
		
		vertices3 = GeomVertexWriter(data, "vertex") # Vertices for flat walls
		texcoord3 = GeomVertexWriter(data, 'texcoord')
		
		vertices4 = GeomVertexWriter(data, "vertex") # Vertices for outward corners
		texcoord4 = GeomVertexWriter(data, 'texcoord')
>>>>>>> 74554ef4d9637471809b863439f18ab0c766b406
		
		self.loadLight()
			
	def loadLight(self): #Sets the lights
		plight = AmbientLight('my plight')
		plight.setColor(VBase4(1.0,1.0,1.0,0.5))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)
