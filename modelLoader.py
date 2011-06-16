from pandac.PandaModules import *

class modelLoader:
	def __init__(self, mapList):
		self.mapList = mapList
		tileX = 0
		tileY = 0
		for row in mapList:
		
			for tile in row:
				tile.model = self.makeModel(tile)
				tile.posX = tileX
				tile.posY = tileY
				tile.model.setPos(tile.posX,tile.posY,0)
				tex=loader.loadTexture(tile.texture)
				# print tex
				tile.model.setTexture(tex, 1)
				
				tileX += 4
				
			tileX = 0
			tileY += 4
			
		print 'END OF MODEL LOADER!'
			
	def makeModel(self, tileData):
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
			node = GeomNode("Solid") 
			node.addGeom(geom)
			
			return NodePath(node)
				
			#return mapList
			
		if (tileData.solid == True):
			model = makeTile(tileData)
		else:
			model = makeSolid(tileData)
			
		#print model
		model.reparentTo(render)
		model.flattenStrong()
		
		return model
