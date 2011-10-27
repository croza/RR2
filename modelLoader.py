from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

import copy
import random

class modelLoader(DirectObject):	
	#def __init__(self, mainClass.parserClass, mainClass.mapLoaderClass): # Basically an __init__, but not run every time that this is called
	def __init__(self, mainClass):
#		self.mapList = mapList
		self.mapX = mainClass.mapLoaderClass.mapConfigParser.getint("map", "width")
		self.mapY = mainClass.mapLoaderClass.mapConfigParser.getint("map", "height")
		
		tileNumber = 0
		tileX = 0
		tileY = 0
		for row in mainClass.mapLoaderClass.tileArray: # Self explanitary
			for tile in row: # For each tile in row, make a model, and position it
				tile.posX = tileX
				tile.posY = tileY
				
				mapData = self.loadSurroundings(mainClass, tileX/4, tileY/4) # aroundInfo: BL, BC, BR, L, C, R, TL, TC, TR. cornerMap: BL, BR, TL, TR
				
				tile.solidMap = mapData[0]
				tile.cornerMap = mapData[1]
				
				tile.model = self.makeModel(tile, mainClass)
					
				tile.model.setCollideMask(BitMask32.bit(0))
					
				tile.model.reparentTo(render)
				tile.model.setPos(tile.posX,tile.posY,0)#tile.posZ)
				
				tile.model.flattenStrong()
				
				tex=loader.loadTexture(tile.texture)
				tile.model.setTexture(tex, 1)
				
				tileX += 4
				tileNumber += 1
				
			tileX = 0
			tileY += 4
			
	def addObject(self, mainClass, objectID, tile):
		position = (tile.posX-2+random.randint(0,3)+random.random(), tile.posY-2+random.randint(0,3)+random.random(), 10)
		mainClass.gameObjects[mainClass.gameObjectID] = copy.copy(mainClass.parserClass.object[mainClass.parserClass.mainConfig.get('objects', str(objectID))])
		mainClass.gameObjects[mainClass.gameObjectID].modelNode = loader.loadModel(mainClass.gameObjects[mainClass.gameObjectID].model)
		mainClass.gameObjects[mainClass.gameObjectID].modelNode.setPos(position)
		mainClass.gameObjects[mainClass.gameObjectID].modelNode.reparentTo(render)
		mainClass.gameObjects[mainClass.gameObjectID].modelNode.setCollideMask(BitMask32.bit(1))
		
		mainClass.heightColNp.setPos(position[0], position[1], 100)
	
		base.cTrav2.traverse(render)
		
		entries = []
		for i in range(mainClass.heightHandler.getNumEntries()):
			entry = mainClass.heightHandler.getEntry(i)
			entries.append(entry)
		entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
									 x.getSurfacePoint(render).getZ()))	
		
		if (len(entries)>0):
			mainClass.gameObjects[mainClass.gameObjectID].modelNode.setZ(entries[0].getSurfacePoint(render).getZ())

		mainClass.gameObjectID += 1
		
	def reloadSurroundings(self, mainClass, tileChanged):
		aroundInfo = []
		aroundInfo.append(mainClass.mapLoaderClass.tileArray[tileChanged.posY/4-1][tileChanged.posX/4-1])
		aroundInfo.append(mainClass.mapLoaderClass.tileArray[tileChanged.posY/4-1][tileChanged.posX/4])
		aroundInfo.append(mainClass.mapLoaderClass.tileArray[tileChanged.posY/4-1][tileChanged.posX/4+1])
		
		aroundInfo.append(mainClass.mapLoaderClass.tileArray[tileChanged.posY/4][tileChanged.posX/4-1])
		aroundInfo.append(mainClass.mapLoaderClass.tileArray[tileChanged.posY/4][tileChanged.posX/4+1])
		
		aroundInfo.append(mainClass.mapLoaderClass.tileArray[tileChanged.posY/4+1][tileChanged.posX/4-1])
		aroundInfo.append(mainClass.mapLoaderClass.tileArray[tileChanged.posY/4+1][tileChanged.posX/4])
		aroundInfo.append(mainClass.mapLoaderClass.tileArray[tileChanged.posY/4+1][tileChanged.posX/4+1])
		
		for around in aroundInfo:
			around.solidMap = self.reloadSolidMap(mainClass, around.posX/4, around.posY/4)
			around.model.detachNode()
			
			around.model = self.makeModel(around)
			around.model.setCollideMask(0x01)
			
			around.model.reparentTo(render)
			around.model.setPos(around.posX, around.posY, 0)
			
			tex = loader.loadTexture(around.texture)
			around.model.setTexture(tex, 1)
				
	def reloadSolidMap(self, mainClass, tileX, tileY):
		solidMap = []
		
		yBehind = tileY - 1
		yInfront = tileY +1
		
		xBehind = tileX - 1
		xInfront = tileX + 1
		
		if (yInfront >= self.mapY-1):
			yInfront = self.mapY-1
			
		if (yBehind <= 0):
			yBehind = 0
			
		if (xInfront >= self.mapX-1):
			xInfront = self.mapX-1
			
		if (xBehind <= 0):
			xBehind = 0
		
		bottomLeft = mainClass.mapLoaderClass.tileArray[yBehind][xBehind].solid
		bottomCentre = mainClass.mapLoaderClass.tileArray[yBehind][tileX].solid
		bottomRight = mainClass.mapLoaderClass.tileArray[yBehind][xInfront].solid
		
		left = mainClass.mapLoaderClass.tileArray[tileY][xBehind].solid
		current = mainClass.mapLoaderClass.tileArray[tileY][tileX].solid
		right = mainClass.mapLoaderClass.tileArray[tileY][xInfront].solid
		
		topLeft = mainClass.mapLoaderClass.tileArray[yInfront][xBehind].solid
		topCentre = mainClass.mapLoaderClass.tileArray[yInfront][tileX].solid
		topRight = mainClass.mapLoaderClass.tileArray[yInfront][xInfront].solid
		
		solidMap.append(bottomLeft)#.solid)
		solidMap.append(bottomCentre)#.solid)
		solidMap.append(bottomRight)#.solid)
		solidMap.append(left)#.solid)
		solidMap.append(current)#.solid)
		solidMap.append(right)#.solid)
		solidMap.append(topLeft)#.solid)
		solidMap.append(topCentre)#.solid)
		solidMap.append(topRight)#.solid)
			
		return solidMap
	
	def loadSurroundings(self, mainClass, tileX, tileY): # Returns a list of the surrounding slids
		def try1(xToTry, yToTry, currentX, currentY): # Tries the tile to see if it exists, and if it does returns the tile, else it returns the current tile
			try:
				returnTile = mainClass.mapLoaderClass.tileArray[yToTry][xToTry]
			except:
				returnTile = mainClass.mapLoaderClass.tileArray[currentY][currentX]
			return returnTile
			
		def makeCornerMap(heightMap): # Makes the points of the corners from the heightmap. Makes an average of the 4 squares for each corner.
			cornerMap = []
			cornerMap.append((heightMap[0]+heightMap[1]+heightMap[3]+heightMap[4])/4) # BL
			cornerMap.append((heightMap[1]+heightMap[2]+heightMap[4]+heightMap[5])/4) # BR
			cornerMap.append((heightMap[4]+heightMap[5]+heightMap[7]+heightMap[8])/4) # TR
			cornerMap.append((heightMap[3]+heightMap[4]+heightMap[6]+heightMap[7])/4) # TL
			return cornerMap
			
		surroundMap = []
		heightMap = []
		
		bottomLeft = try1(tileX-1, tileY-1, tileX, tileY)
		bottomCentre = try1(tileX, tileY-1, tileX, tileY)
		bottomRight = try1(tileX+1, tileY-1, tileX, tileY)
		left = try1(tileX-1, tileY, tileX, tileY)
		current = mainClass.mapLoaderClass.tileArray[tileY][tileX]
		right = try1(tileX+1, tileY, tileX, tileY)
		topLeft = try1(tileX-1, tileY+1, tileX, tileY)
		topCentre = try1(tileX, tileY+1, tileX, tileY)
		topRight = try1(tileX+1, tileY+1, tileX, tileY)
		
		surroundMap.append(bottomLeft.solid) # 0
		surroundMap.append(bottomCentre.solid) # 1
		surroundMap.append(bottomRight.solid) # 2
		surroundMap.append(left.solid) # 3
		surroundMap.append(current.solid) # 4
		surroundMap.append(right.solid) # 5
		surroundMap.append(topLeft.solid) # 6
		surroundMap.append(topCentre.solid) # 7
		surroundMap.append(topRight.solid) # 8
		
		heightMap.append(bottomLeft.posZ/2)
		heightMap.append(bottomCentre.posZ/2)
		heightMap.append(bottomRight.posZ/2)
		heightMap.append(left.posZ/2)
		heightMap.append(current.posZ/2)
		heightMap.append(right.posZ/2)
		heightMap.append(topLeft.posZ/2)
		heightMap.append(topCentre.posZ/2)
		heightMap.append(topRight.posZ/2)
		
		cornerMap = makeCornerMap(heightMap)
		
		return (surroundMap, cornerMap)
			
	def makeModel(self, tileData, mainClass): # The function to make a model
		def makeTile(tileData):
			x = tileData.posX/4
			y = tileData.posY/4
			
			if (len(str(x)) == 1):
				x = '0'+str(x)
			else:
				x = str(x)
				
			if (len(str(y)) == 1):
				y = '0'+str(y)
			else:
				y = str(y)
			format = GeomVertexFormat.getV3n3c4t2()
			data = GeomVertexData("Data", format, Geom.UHStatic) 
			
			vertices = GeomVertexWriter(data, "vertex") # Vertices for just a plane tile
			texcoord = GeomVertexWriter(data, 'texcoord')
			
			triangles = GeomTriangles(Geom.UHStatic)
			
			vertices.addData3f(-2, -2, tileData.cornerMap[0]) # 0: BL
			texcoord.addData2f(0,0)
			vertices.addData3f(2, -2, tileData.cornerMap[1]) # 1: BR
			texcoord.addData2f(1,0)
			vertices.addData3f(2, 2, tileData.cornerMap[2]) # 2: TR
			texcoord.addData2f(1,1)
			vertices.addData3f(-2, 2, tileData.cornerMap[3]) # 3: TL
			texcoord.addData2f(0,1)
			
			triangles.addVertices(0, 1, 3) # Remember that this works in an anti-clockwise rotation
			triangles.addVertices(1, 2, 3) # This stuff is drawing the triangles for each square
			triangles.closePrimitive()
			
			geom = Geom(data) 

			geom.addPrimitive(triangles) 
			
			if (tileData.water == True):
				tileData.modelName = 'water '+str(x).zfill(2)+', '+str(y).zfill(2)
			elif (tileData.lava == True):
				tileData.modelName = 'lava '+str(x).zfill(2)+', '+str(y).zfill(2)
			else:
				tileData.modelName = 'tile '+str(x).zfill(2)+', '+str(y).zfill(2)
			
			node = GeomNode(tileData.modelName) 
			node.addGeom(geom)
			
#			tileData.modelName = 'tile'
			
			return NodePath(node) 
			
		def makeSolid(tileData, mainClass):
			def makeFlat(v0, v1, v2, v3):
				vertices3.addData3f(v0) # UBL
				texcoord3.addData2f(0, 0)
				vertices3.addData3f(v1) # UBR
				texcoord3.addData2f(1, 0)
				vertices3.addData3f(v2) # UTR
				texcoord3.addData2f(1, 1)
				vertices3.addData3f(v3) # UTL
				texcoord3.addData2f(0, 1)
				
				solids.addVertices(0, 1, 3)
				solids.addVertices(1, 2, 3)
				solids.closePrimitive()
				
			def makeSlant(v0, v1, v2, v3):
				vertices3.addData3f(v0) # UBL
				texcoord3.addData2f(0, 0)
				vertices3.addData3f(v1) # UBR
				texcoord3.addData2f(1, 0)
				vertices3.addData3f(v2) # UTR
				texcoord3.addData2f(1, 1)
				vertices3.addData3f(v3) # UTL
				texcoord3.addData2f(0, 1)
				
				solids.addVertices(0, 1, 3)
				solids.addVertices(1, 2, 3)
				solids.closePrimitive()
				
			def makeCorner( v0, v1, v2, v3, v4):
				vertices3.addData3f(v0) # 0
				texcoord3.addData2f(0, 1)
				vertices3.addData3f(v1) # 1
				texcoord3.addData2f(1, 1)
				vertices3.addData3f(v2) # 2
				texcoord3.addData2f(0, 0)
				vertices3.addData3f(v3) # 3
				texcoord3.addData2f(1, 0)
				vertices3.addData3f(v3) # 4
				texcoord3.addData2f(0, 0)
				vertices3.addData3f(v4) # 5
				texcoord3.addData2f(1, 0)
				
				solids.addVertices(0, 2, 3)
				solids.addVertices(1, 4, 5)
				solids.closePrimitive()
				
			def makeOtherCorner(v0, v1, v2, v3, v4, v5):
				vertices3.addData3f(v0)
				texcoord3.addData2f(1, 1)
				vertices3.addData3f(v1)
				texcoord3.addData2f(0, 1)
				vertices3.addData3f(v2) 
				texcoord3.addData2f(0, 1)
				vertices3.addData3f(v3) 
				texcoord3.addData2f(0, 0)
				vertices3.addData3f(v4) 
				texcoord3.addData2f(1, 0)
				vertices3.addData3f(v5) 
				texcoord3.addData2f(1, 1)
				
				solids.addVertices(0, 2, 3)
				solids.addVertices(1, 4, 5)
				solids.closePrimitive()
				
			x = tileData.posX/4
			y = tileData.posY/4
			
			if (len(str(x)) == 1):
				x = '0'+str(x)
			else:
				x = str(x)
				
			if (len(str(y)) == 1):
				y = '0'+str(y)
			else:
				y = str(y)
				
			format = GeomVertexFormat.getV3n3c4t2()
			data = GeomVertexData("Data", format, Geom.UHStatic) 
			
			vertices3 = GeomVertexWriter(data, "vertex") # Vertices for just a plane tile
			texcoord3 = GeomVertexWriter(data, 'texcoord')
			
			solids = GeomTriangles(Geom.UHStatic)
			
			vertex0 = (-2, -2, tileData.cornerMap[0]) # 0 Bottom Left
			vertex1 = (-2, -2, tileData.cornerMap[0]+4) # 1 Upper Bottom Left
			vertex2 = (2, -2, tileData.cornerMap[1]) # 2 Bottom Right
			vertex3 = (2, -2, tileData.cornerMap[1]+4) # 3 Upper Bottom Right
			vertex4 = (2, 2, tileData.cornerMap[2]) # 4 Top Right
			vertex5 = (2, 2, tileData.cornerMap[2]+4) # 5 Upper Top Right
			vertex6 = (-2, 2, tileData.cornerMap[3]) # 6 Top Left
			vertex7 = (-2, 2, tileData.cornerMap[3]+4) # 7 Upper Top Left
			
			if (tileData.solidMap[0] == True and 
			tileData.solidMap[1] == True and 
			tileData.solidMap[2] == True and 
			tileData.solidMap[3] == True and 
			tileData.solidMap[5] == True and 
			tileData.solidMap[6] == True and 
			tileData.solidMap[7] == True and 
			tileData.solidMap[8] == True): # If all the surroundings are solids
				makeFlat(vertex1, vertex3, vertex5, vertex7)
				tileData.modelName = 'solid roof '+str(x).zfill(2)+', '+str(y).zfill(2)
				tileData.texture2 = 'data/models/world/textures/roof.png'
			
			elif (tileData.solidMap[0] == True and 
			tileData.solidMap[1] == True and 
			tileData.solidMap[2] == True and 
			tileData.solidMap[3] == True and 
			tileData.solidMap[5] == True and 
			tileData.solidMap[7] == False): # A sloped tile facing north
				makeSlant(vertex4, vertex6, vertex1, vertex3)
				tileData.modelName = 'solid slope north '+str(x).zfill(2)+', '+str(y).zfill(2)

			elif (tileData.solidMap[1] == True and 
			tileData.solidMap[2] == True and 
			tileData.solidMap[3] == False and 
			tileData.solidMap[5] == True and 
			tileData.solidMap[7] == True and
			tileData.solidMap[8] == True): # A sloped tile facing west
				makeSlant(vertex6, vertex0, vertex3, vertex5)
				tileData.modelName = 'solid slope west '+str(x).zfill(2)+', '+str(y).zfill(2)
				
			elif (tileData.solidMap[1] == False and 
			tileData.solidMap[3] == True and 
			tileData.solidMap[5] == True and 
			tileData.solidMap[6] == True and 
			tileData.solidMap[7] == True and 
			tileData.solidMap[8] == True): # A sloped tile facing south
				makeSlant(vertex0, vertex2, vertex5, vertex7)
				tileData.modelName = 'solid slope south '+str(x).zfill(2)+', '+str(y).zfill(2)

			elif (tileData.solidMap[0] == True and 
			tileData.solidMap[1] == True and 
			tileData.solidMap[3] == True and 
			tileData.solidMap[5] == False and 
			tileData.solidMap[6] == True and 
			tileData.solidMap[7] == True): # A sloped tile facing east
				makeSlant(vertex2, vertex4, vertex7, vertex1)
				tileData.modelName = 'solid slope east '+str(x).zfill(2)+', '+str(y).zfill(2)

			elif (tileData.solidMap[1] == False and 
			tileData.solidMap[3] == False and 
			tileData.solidMap[5] == True and 
			tileData.solidMap[7] == True and 
			tileData.solidMap[8] == True): # A corner with solids north, and east
				makeCorner(vertex5, vertex5, vertex6, vertex0, vertex2)
				tileData.modelName = 'solid corner1 north, east '+str(x).zfill(2)+', '+str(y).zfill(2)
			
			elif (tileData.solidMap[1] == False and 
			tileData.solidMap[3] == True and 
			tileData.solidMap[5] == False and 
			tileData.solidMap[6] == True and 
			tileData.solidMap[7] == True): # A corner with solids north, and west
				makeCorner(vertex7, vertex7, vertex0, vertex2, vertex4)
				tileData.modelName = 'solid corner1 north, west '+str(x).zfill(2)+', '+str(y).zfill(2)
				
			elif (tileData.solidMap[0] == True and 
			tileData.solidMap[1] == True and 
			tileData.solidMap[3] == True and 
			tileData.solidMap[5] == False and 
			tileData.solidMap[7] == False): # A corner with solids south, and west
				makeCorner(vertex1, vertex1, vertex2, vertex4, vertex6)
				tileData.modelName = 'solid corner1 south, west '+str(x).zfill(2)+', '+str(y).zfill(2)
				
			elif (tileData.solidMap[1] == True and 
			tileData.solidMap[2] == True and 
			tileData.solidMap[3] == False and 
			tileData.solidMap[5] == True and 
			tileData.solidMap[7] == False): # A corner with solids south, and east
				makeCorner(vertex3, vertex3, vertex4, vertex6, vertex0)
				tileData.modelName = 'solid corner1 south, east '+str(x).zfill(2)+', '+str(y).zfill(2)
				
			elif (tileData.solidMap[0] == True and 
			tileData.solidMap[1] == True and 
			tileData.solidMap[2] == True and 
			tileData.solidMap[3] == True and 
			tileData.solidMap[5] == True and 
			tileData.solidMap[6] == True and 
			tileData.solidMap[7] == True and
			tileData.solidMap[8] == False): # Another corner north and east
				makeOtherCorner(vertex1, vertex1, vertex3, vertex4, vertex4, vertex7)
				tileData.modelName = 'solid corner2 north, east '+str(x).zfill(2)+', '+str(y).zfill(2)

			elif (tileData.solidMap[0] == True and 
			tileData.solidMap[1] == True and 
			tileData.solidMap[2] == True and 
			tileData.solidMap[3] == True and 
			tileData.solidMap[5] == True and 
			tileData.solidMap[6] == False and 
			tileData.solidMap[7] == True and
			tileData.solidMap[8] == True): # Another corner north and west
				makeOtherCorner(vertex3, vertex3, vertex5, vertex6, vertex6, vertex1)
				tileData.modelName = 'solid corner2 north, west '+str(x).zfill(2)+', '+str(y).zfill(2)
			
			elif (tileData.solidMap[0] == False and 
			tileData.solidMap[1] == True and 
			tileData.solidMap[2] == True and 
			tileData.solidMap[3] == True and 
			tileData.solidMap[5] == True and 
			tileData.solidMap[6] == True and 
			tileData.solidMap[7] == True and
			tileData.solidMap[8] == True): # Another corner south and west
				makeOtherCorner(vertex5, vertex5, vertex7, vertex0, vertex0, vertex3)
				tileData.modelName = 'solid corner2 south, west '+str(x).zfill(2)+', '+str(y).zfill(2)
				
			elif (tileData.solidMap[0] == True and 
			tileData.solidMap[1] == True and 
			tileData.solidMap[2] == False and 
			tileData.solidMap[3] == True and 
			tileData.solidMap[5] == True and 
			tileData.solidMap[6] == True and 
			tileData.solidMap[7] == True and
			tileData.solidMap[8] == True): # Another corner south and east
				makeOtherCorner(vertex7, vertex7, vertex1, vertex2, vertex2, vertex5)
				tileData.modelName = 'solid corner2 south, east '+str(x).zfill(2)+', '+str(y).zfill(2)
			
			elif (tileData.solidMap[0] == True and # An odd bridge thing...
			tileData.solidMap[1] == True and
			tileData.solidMap[2] == False and
			tileData.solidMap[3] == True and
			tileData.solidMap[5] == True and
			tileData.solidMap[6] == False and
			tileData.solidMap[7] == True and
			tileData.solidMap[8] == True):
				makeFlat(vertex6, vertex1, vertex2, vertex5)
				tileData.modelName = 'solid bridge at '+str(x).zfill(2)+', '+str(y).zfill(2)
				
			elif (tileData.solidMap[0] == False and # An odd bridge thing...
			tileData.solidMap[1] == True and
			tileData.solidMap[2] == True and
			tileData.solidMap[3] == True and
			tileData.solidMap[5] == True and
			tileData.solidMap[6] == True and
			tileData.solidMap[7] == True and
			tileData.solidMap[8] == False):
				makeFlat(vertex0, vertex3, vertex4, vertex7)
				tileData.modelName = 'solid bridge at '+str(x).zfill(2)+', '+str(y).zfill(2)
			
			else:
				makeFlat(vertex0, vertex2, vertex4, vertex6)
				tileData.modelName = 'solid no work '+str(x).zfill(2)+', '+str(y).zfill(2)
				#mainClass.mineWall(tileData)
				
			geom = Geom(data) 
			try:
				geom.addPrimitive(solids) 
			except:
				print 'No  geom'
			node = GeomNode(tileData.modelName)
			node.addGeom(geom)
			
			return NodePath(node)
			
		if (tileData.solid == True):
			model = makeSolid(tileData, mainClass)
		else:
			model = makeTile(tileData)
		
		return model