import os, sys, math, random

import random
import mapLib
import config
import wallTypes
import moving2
import ConfigParser
import StringIO

from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import AmbientLight, DirectionalLight
from pandac.PandaModules import VBase4, VBase3
import direct.directbase.DirectStart

from pandac.PandaModules import *

class world(DirectObject):
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
		
		print heightMap
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
		
		vertices5 = GeomVertexWriter(data, "vertex") # Vertices for roofs
		texcoord5 = GeomVertexWriter(data, 'texcoord')
		
		vertices6 = GeomVertexWriter(data, "vertex") # Vertices for inward corners
		texcoord6 = GeomVertexWriter(data, 'texcoord')
		
		triangles = GeomTriangles(Geom.UHStatic)
		solids = GeomTriangles(Geom.UHStatic)
		
		size = 2 # Half the size of the square
		
		def addTile(left, right, topRight, topLeft): # v0 is bottom left, anticlockwise
			vertices.addData3f(left[0], left[1], left[2])
			texcoord.addData2f(0,0)
			vertices.addData3f(right[0], right[1], right[2])
			texcoord.addData2f(0,0)
			vertices.addData3f(topRight[0], topRight[1], topRight[2])
			texcoord.addData2f(0,0)
			vertices.addData3f(topLeft[0], topLeft[1], topLeft[2])
			texcoord.addData2f(0,0)
			
			triangles.addVertices(0, 1, 3) # Remember that this works in an anti-clockwise rotation
			triangles.addVertices(1, 2, 3) # This stuff is drawing the triangles for each square
			triangles.closePrimitive()
			
		def addSolid(size, tile, around, bottomLeft1, upperBottomLeft1, bottomRight1, upperBottomRight1, topRight1, upperTopRight1, topLeft1, upperTopLeft1):		# Starts in the bottom left, anti-clockwise, ends with the top
				
			def plainWall(lowerLeft, lowerRight, upperRight, upperLeft): # Adds a plain, flat, wall. v0 being the lowest left, anti-clockwise
				vertices3.addData3f(lowerLeft[0], lowerLeft[1], lowerLeft[2])
				texcoord3.addData2f(0,0)
				vertices3.addData3f(lowerRight[0], lowerRight[1], lowerRight[2])
				texcoord3.addData2f(1,0)
				vertices3.addData3f(upperRight[0], upperRight[1], upperRight[2])
				texcoord3.addData2f(1,1)
				vertices3.addData3f(upperLeft[0], upperLeft[1], upperLeft[2])
				texcoord3.addData2f(0,1)
				
				solids.addVertices(0, 1, 3) # The most left triangle
				solids.addVertices(1, 2, 3)
				solids.closePrimitive()
			
			def cornerOut(top, vertex1, vertex2, vertex3): # top is the highest point, with v1 being the lest anti-clockwise (??)
				vertices4.addData3f(top[0], top[1], top[2])
				texcoord4.addData2f(0,1)
				vertices4.addData3f(top[0], top[1], top[2]) # Two tops to deal with a UV thing... the top can't be two points at once otherwise
				texcoord4.addData2f(1,1)
				vertices4.addData3f(vertex1[0], vertex1[1], vertex1[2])
				texcoord4.addData2f(0,0)
				vertices4.addData3f(vertex2[0], vertex2[1], vertex2[2])
				texcoord4.addData2f(0.5,0)
				vertices4.addData3f(vertex3[0], vertex3[1], vertex3[2])
				texcoord4.addData2f(0,1)
				
				solids.addVertices(0, 2, 3)
				solids.addVertices(3, 4, 1)
				solids.closePrimitive()
				
			def cornerIn(top, vertex1, vertex2, vertex3): # Same with the top as above, although also repeated with point 2. vertex2 is the lowest
				vertices6.addData3f(top[0], top[1], top[2])
				texcoord6.addData2f(0,1)
				vertices6.addData3f(top[0], top[1], top[2])
				texcoord6.addData2f(0,1)
				vertices6.addData3f(vertex1[0], vertex1[1], vertex1[2])
				texcoord6.addData2f(0,1)
				vertices6.addData3f(vertex2[0], vertex2[1], vertex2[2])
				texcoord6.addData2f(0,1)
				vertices6.addData3f(vertex2[0], vertex2[1], vertex2[2])
				texcoord6.addData2f(0,1)
				vertices6.addData3f(vertex3[0], vertex3[1], vertex3[2])
				texcoord6.addData2f(0,1)
				
				solids.addVertices(0, 2, 3)
				solids.addVertices(1, 4, 5)
				
			def roof(Left, Right, upperLeft, upperRight):
				UBL = Left
				UBR = Right
				UTR = upperLeft
				UTL = upperRight
				start = UTL[2]
				
				if(around[4] == 0): # Below Left
					UBL[2] = bottomLeft1[2]
				if(around[5] == 0): # Below Right
					UBR[2] = bottomRight1[2]
				if(around[6] == 0): # Above Right
					UTR[2] = topRight1[2]
				if(around[4] == 0): # Above Left
					UTL[2] = topLeft1[2]
				
				vertices5.addData3f(Left[0], Left[1], Left[2])
				texcoord5.addData2f(0,0)
				vertices5.addData3f(Right[0], Right[1], Right[2])
				texcoord5.addData2f(1,0)
				vertices5.addData3f(upperLeft[0], upperLeft[1], upperLeft[2])
				texcoord5.addData2f(1,1)
				vertices5.addData3f(upperRight[0], upperRight[1], upperRight[2])
				texcoord5.addData2f(0,1)
				
				solids.addVertices(0, 1, 3)
				solids.addVertices(1, 2, 3)
				solids.closePrimitive()
				
			diagonals = 0
				
			if (around[4] == 0):
				diagonals += 1
				print 'o'
			elif (around[5] == 0):
				diagonals += 1
				print 'p'
			elif (around[6] == 0):
				diagonals += 1
			elif (around[7] == 0):
				diagonals += 1
				
			if (diagonals >= 2):
				tile.solid = False
				addTile(bottomLeft1, bottomRight1, topRight1, topLeft1) # Call to make a tile
				
			elif ((around[0] == 1) and (around[1] == 0) and (around[2] == 1) and (around[3] == 1) and (around[6] == 1)): # Slanting to the left (with the camera looking from the 'bottom' of the map upwards)
				plainWall(topLeft1, bottomLeft1, upperBottomRight1, upperTopRight1)
				
			elif ((around[0] == 1) and (around[1] == 1) and (around[2] == 1) and (around[3] == 0)): # Slanting to the right
				plainWall(bottomRight1, topRight1, upperTopLeft1, upperBottomLeft1)
				
			elif ((around[0] == 1) and (around[1] == 1) and (around[2] == 0) and (around[3] == 1)): # Slanting downwards
				plainWall(bottomLeft1, bottomRight1, upperTopRight1, upperTopLeft1)
				
			elif ((around[0] == 0) and (around[1] == 1) and (around[2] == 1) and (around[3] == 1)): # Slanting upwards
				plainWall(topRight1, topLeft1, upperBottomLeft1, upperBottomRight1)
				
			elif ((around[0] == 1) and (around[1] == 0) and (around[2] == 0) and (around[3] == 1)): # Corner, if Above and Left
				cornerOut(upperTopRight1, topLeft1, bottomLeft1, bottomRight1)
			
			elif ((around[0] == 1) and (around[1] == 1) and (around[2] == 0) and (around[3] == 0)): # Corner, if Above and Right
				cornerOut(upperTopLeft1, bottomLeft1, bottomRight1, topRight1)
				
			elif ((around[0] == 0) and (around[1] == 1) and (around[2] == 1) and (around[3] == 0)): # Corner, if Below and Left
				cornerOut(upperBottomLeft1, bottomRight1, topRight1, topLeft1)
				
			elif ((around[0] == 0) and (around[1] == 0) and (around[2] == 1) and (around[3] == 1)): # Corner, if Below and Right
				cornerOut(upperBottomRight1, topRight1, topLeft1, bottomLeft1)
				
			elif ((around[0] == 0) and (around[1] == 0) and (around[2] == 1) and (around[3] == 1) and (around[6] == 0)): # Corner, if Above and Left (outwards)
				cornerIn(upperBottomRight1, upperTopRight1, topLeft1, upperBottomLeft1)
				
			elif ((around[0] == 1) and (around[1] == 1) and (around[2] == 1) and (around[3] == 1)): # All solid
				# UBL = upperBottomLeft1
				# UBR = upperBottomRight1
				# UTR = upperTopRight1
				# UTL = upperTopLeft1
				# start = UTL[2]
				# if(around[4] == 0): # Below Left
					# UBL[2] = bottomLeft1[2]
				# if(around[5] == 0): # Below Right
					# UBR[2] = bottomRight1[2]
				# if(around[6] == 0): # Above Right
					# UTR[2] = topRight1[2]
				# if(around[4] == 0): # Above Left
					# UTL[2] = topLeft1[2]
				
				# if(UTL[2] != start):
					# print UTR[2], start
				
				roof(upperBottomLeft1, upperBottomRight1, upperTopRight1, upperTopLeft1)
				
		triData = list[number]		
		bottomLeft = triData[0]# Getting the height data out of the list
		bottomRight = triData[1]
		topRight = triData[2]
		topLeft = triData[3]
		
		bottomLeft1 = [-size, -size, bottomLeft/2] # 0 BottomLeft
		upperBottomLeft1 = [-size, -size, float(bottomLeft/2+2*size)] # 1 BLT (bottom left top)
		bottomRight1 = [size, -size, bottomRight/2] # 2 BR
		upperBottomRight1 = [size, -size, bottomRight/2+2*size] # 3 BRT
		topRight1 = [size, size, topRight/2] # 4 TR
		upperTopRight1 = [size, size, topRight/2+2*size] # 5 TRT
		topLeft1 = [-size, +size, topLeft/2] # 6 TL
		upperTopLeft1 = [-size, size, topLeft/2+2*size] #7 TLT
			
		vertices.addData3f(-size, -size, bottomLeft/2) # 0 ## This bit is adding the vertices to make triangles out of the vertecies to make a flat tile
		texcoord.addData2f(0,0)
		vertices.addData3f(size, -size, bottomRight/2) # 1st
		texcoord.addData2f(1,0)
		vertices.addData3f(size, size, topRight/2) # 2nd
		texcoord.addData2f(1,1)
		vertices.addData3f(-size, +size, topLeft/2) # 3rd
		texcoord.addData2f(0,1)
		
		addTile(bottomLeft1, bottomRight1, topRight1, topLeft1) # Call to make a tile
		
		if tile.solid == True:
			addSolid(size, tile, around, bottomLeft1, upperBottomLeft1, bottomRight1, upperBottomRight1, topRight1, upperTopRight1, topLeft1, upperTopLeft1)
			geom = Geom(data) 
			try:
				geom.addPrimitive(solids) 
			except:
				print 'r'
			node = GeomNode("Solid") 
			node.addGeom(geom)
		
		else:
			geom = Geom(data) 

			geom.addPrimitive(triangles) 
			node = GeomNode("Tile") 
			node.addGeom(geom)
		
		return NodePath(node) 
		
	def loadLight(self): #Sets the lights
		plight = AmbientLight('my plight')
		plight.setColor(VBase4(0.6,0.6,0.6,0.5))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)