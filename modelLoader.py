from pandac.PandaModules import *

class modelLoader:	
	def runOnceLoadModels(self, mapList, mapX): # Basically an __init__, but not run every time that this is called
		self.mapList = mapList
		tileNumber = 0
		tileX = 0
		tileY = 0
		for row in mapList: # Self explanitary
			for tile in row: # For each tile in row, make a model, and position it
				tile.posX = tileX
				tile.posY = tileY
				
				mapData = self.loadSurroundings(mapX, tileX/4, tileY/4) # aroundInfo: BL, BC, BR, L, C, R, TL, TC, TR. cornerMap: BL, BR, TL, TR
				
				tile.solidMap = mapData[0]
				tile.cornerMap = mapData[1]
				
				tile.model = self.makeModel(tile)
				
				tile.model.reparentTo(render)
				tile.model.setPos(tile.posX,tile.posY,0)#tile.posZ)
				
				tex=loader.loadTexture(tile.texture)
				tile.model.setTexture(tex, 1)
				tileX += 4
				tileNumber += 1
				
			tileX = 0
			tileY += 4
			
		return mapList
		
	def loadSurroundings(self, mapX, tileX, tileY): # Returns a list of the surrounding slids
		def try1(xToTry, yToTry, currentX, currentY): # Tries the tile to see if it exists, and if it does returns the tile, else it returns the current tile
			try:
				returnTile = self.mapList[yToTry][xToTry]
			except:
				returnTile = self.mapList[currentY][currentX]
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
		current = self.mapList[tileY][tileX]
		right = try1(tileX+1, tileY, tileX, tileY)
		topLeft = try1(tileX-1, tileY+1, tileX, tileY)
		topCentre = try1(tileX, tileY+1, tileX, tileY)
		topRight = try1(tileX+1, tileY+1, tileX, tileY)
		
		surroundMap.append(bottomLeft.solid)
		surroundMap.append(bottomCentre.solid)
		surroundMap.append(bottomRight.solid)
		surroundMap.append(left.solid)
		surroundMap.append(current.solid)
		surroundMap.append(right.solid)
		surroundMap.append(topLeft.solid)
		surroundMap.append(topCentre.solid)
		surroundMap.append(topRight.solid)
		
		heightMap.append(bottomLeft.posZ)
		heightMap.append(bottomCentre.posZ)
		heightMap.append(bottomRight.posZ)
		heightMap.append(left.posZ)
		heightMap.append(current.posZ)
		heightMap.append(right.posZ)
		heightMap.append(topLeft.posZ)
		heightMap.append(topCentre.posZ)
		heightMap.append(topRight.posZ)
		
		cornerMap = makeCornerMap(heightMap)
		
		return (surroundMap, cornerMap)
			
	def makeModel(self, tileData): # The function to make a model
		def makeTile(tileData):
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
			node = GeomNode("Tile") 
			node.addGeom(geom)
			
			return NodePath(node) 
			
		def makeSolid(tileData):
			format = GeomVertexFormat.getV3n3c4t2()
			data = GeomVertexData("Data", format, Geom.UHStatic) 
			
			vertices3 = GeomVertexWriter(data, "vertex") # Vertices for just a plane tile
			texcoord3 = GeomVertexWriter(data, 'texcoord')
			
			solids = GeomTriangles(Geom.UHStatic)
		
			vertices3.addData3f(-2, -2, tileData.cornerMap[0]) # 0
			texcoord3.addData2f(0,0)
			vertices3.addData3f(2, -2, tileData.cornerMap[1]) # 1
			texcoord3.addData2f(1,0)
			vertices3.addData3f(2, 2, tileData.cornerMap[2]) # 2
			texcoord3.addData2f(1,1)
			vertices3.addData3f(-2, 2, tileData.cornerMap[3]) # 3
			texcoord3.addData2f(0,1)
			
			solids.addVertices(0, 1, 3) # The most left triangle
			solids.addVertices(1, 2, 3)
			solids.closePrimitive()
			
			geom = Geom(data) 
			try:
				geom.addPrimitive(solids) 
			except:
				print 'No  geom'
			node = GeomNode("Solid at"+str(tileData.posX)+','+str(tileData.posY))
			node.addGeom(geom)
			
			return NodePath(node)
			
		if (tileData.solid == True):
			model = makeTile(tileData)
		else:
			model = makeSolid(tileData)
		
		return model