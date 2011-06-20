from pandac.PandaModules import *

class modelLoader:	
	def runOnceLoadModels(self, mapList):
		self.mapList = mapList
		tileX = 0
		tileY = 0
		for row in mapList: #Self explanitary
			for tile in row: # For each tile in row, make a model, and position it
				tile.posX = tileX
				tile.posY = tileY
				
				tile.model = self.makeModel(tile)
				
				tile.model.reparentTo(render)
				tile.model.setPos(tile.posX,tile.posY,tile.posZ)
				
				tex=loader.loadTexture(tile.texture)
				tile.model.setTexture(tex, 1)
				tileX += 4
				
			tileX = 0
			tileY += 4
			
		return mapList
			
	def makeModel(self, tileData): # The function to make a model
		def makeTile(tileData):
			format = GeomVertexFormat.getV3n3c4t2()
			data = GeomVertexData("Data", format, Geom.UHStatic) 
			
			vertices = GeomVertexWriter(data, "vertex") # Vertices for just a plane tile
			texcoord = GeomVertexWriter(data, 'texcoord')
			
			triangles = GeomTriangles(Geom.UHStatic)
		
			vertices.addData3f(-2, -2, 0)
			texcoord.addData2f(0,0)
			vertices.addData3f(2, -2, 0)
			texcoord.addData2f(1,0)
			vertices.addData3f(2, 2, 0)
			texcoord.addData2f(1,1)
			vertices.addData3f(-2, 2, 0)
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
		
			vertices3.addData3f(-2, -2, 0)
			texcoord3.addData2f(0,0)
			vertices3.addData3f(2, -2, 0)
			texcoord3.addData2f(1,0)
			vertices3.addData3f(2, 2, 0) #4
			texcoord3.addData2f(1,1)
			vertices3.addData3f(-2, 2, 0) #4
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