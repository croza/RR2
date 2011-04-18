import os, sys, math, random

import random
import mapLib
import config
import wallTypes
import moving2

from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import AmbientLight
from pandac.PandaModules import VBase4
import direct.directbase.DirectStart

from pandac.PandaModules import GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, Geom, GeomNode, NodePath, GeomPoints  # For triangles
from pandac.PandaModules import CollisionTraverser, CollisionHandlerQueue, CollisionNode, BitMask32, CollisionPlane, CollisionSphere, CollisionRay, Plane, Vec3, Point3 # Collision etc.

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
		print heightMap
		w = wallTypes.WorldLoader(heightMap, 10).drawStuff(heightMap, 10) #~# NEEDS FUNCTION TO BE ADDED TO AUTOMATICALLY GET THE SIZE
		ttiles = self.map.generate_tile_array() # The 'data' of all the squares in an array
		# print ttiles
		tileNumber = 0
		tex = loader.loadTexture('data/models/world/textures/ground.png')
		
		for tile in ttiles:
			wallTypes.wallTypes[tile.typeInt].applyCharacteristics(tile)
		
		for tile in ttiles:		
			aroundInfo = [] # The stuff below is to get the data for squares around the current square...
			try:
				above = ttiles[tileNumber+10] #~# SAME HERE
			except:
				above = ttiles[tileNumber]
			try:
				below = ttiles[tileNumber-10]
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
				
			print tileNumber, tile.solid#, ttiles[tileNumber], left.solid
			if(tile.solid == True):
				if(above.solid == True): # Starts above, goes round anti-clockwise, could def something for this...
					aroundInfo.append(1)
				else:
					aroundInfo.append(0)
				if(left.solid == True):
					aroundInfo.append(1)
				else:
					aroundInfo.append(0)
				if(below.solid == True):
					aroundInfo.append(1)
				else:
					aroundInfo.append(0)
				if(right.solid == True):
					aroundInfo.append(1)
				else:
					aroundInfo.append(0)
					
				print aroundInfo
				
			tile.model = self.loadTriangles(w, tileNumber, tile, aroundInfo)
			tile.model.setCollideMask(0x1)
			tile.model.setPos((4*tile.x)-1, (4*tile.y)-1, 0)
			tile.model.reparentTo(render)

			tile.model.setTexture(loader.loadTexture(tile.texture), 1)
			self.tiles.append(tile)
			tileNumber += 1
			
		# print self.tiles
		
	def loadTriangles(self, list, number, tile, around):
		# format = GeomVertexFormat.getV3() 
		format = GeomVertexFormat.getV3n3c4t2()
		data = GeomVertexData("Data", format, Geom.UHStatic) 
		vertices = GeomVertexWriter(data, "vertex") 
		texcoord= GeomVertexWriter(data, 'texcoord')
		size = 2 # Half the size of the square
		
		triangles = GeomTriangles(Geom.UHStatic)
		
		vertices2 = GeomVertexWriter(data, "vertex") 
		texcoord2 = GeomVertexWriter(data, 'texcoord')
		solids = GeomTriangles(Geom.UHStatic)
		
		
		def addTile(v0, v1, v2, v3, v4, v5, v6, v7, v8): # v0 should always be the centre of the tile
			triangles.addVertices(v0, v1, v2) # Remember that this works in an anti-clockwise rotation
			triangles.addVertices(v0, v2, v3) # This stuff is drawing the triangles for each square
			triangles.addVertices(v0, v3, v4)
			triangles.addVertices(v0, v4, v5)
			triangles.addVertices(v0, v5, v6)
			triangles.addVertices(v0, v6, v7)
			triangles.addVertices(v0, v7, v8)
			triangles.addVertices(v0, v8, v1)
			triangles.closePrimitive()
			
		def addSolid(size, tile, around):		# Starts in the bottom left, anti-clockwise, ends with the top
			vertices2.addData3f(-size, -size, bottomLeft/2) # 0 BottomLeft
			texcoord2.addData2f(0,0)
			vertices2.addData3f(-size, -size, bottomLeft+2*size) # 1 BLT (bottom left top)
			texcoord2.addData2f(0,1)
			vertices2.addData3f(0, -size, bottomCentre/2) # 2 BC
			texcoord2.addData2f(0.5,0)
			vertices2.addData3f(size, -size, bottomRight/2) # 3 BR
			texcoord2.addData2f(1,0)
			vertices2.addData3f(size, -size, bottomRight+2*size) # 4 BRT
			texcoord2.addData2f(1,1)
			vertices2.addData3f(size, 0, rightCentre/2) # 5 RC
			texcoord2.addData2f(0.5,0)
			vertices2.addData3f(size, size, topRight/2) # 6 TR
			texcoord2.addData2f(1,0)
			vertices2.addData3f(size, size, topRight+2*size) # 7 TRT
			texcoord2.addData2f(1,1)
			vertices2.addData3f(0, size, topCentre/2) # 8 TC
			texcoord2.addData2f(0.5,0)
			vertices2.addData3f(-size, +size, topLeft/2) # 9 TL
			texcoord2.addData2f(1,0)
			vertices2.addData3f(-size, size, topLeft+2*size) #10 TLT
			texcoord2.addData2f(1,1)
			vertices2.addData3f(-size, 0, leftCentre/2) # 11 LC
			texcoord2.addData2f(0.5,0)
			
			def addSolid2(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11):
				solids.addVertices(v0, v2, v1) # Makes triangles from vertices...
				solids.addVertices(v4, v1, v2)
				solids.addVertices(v2, v3, v4)
				solids.addVertices(v3, v5, v4)
				solids.addVertices(v4, v5, v7)
				solids.addVertices(v5, v6, v7)
				solids.addVertices(v6, v8, v7)
				solids.addVertices(v7, v8, v10)
				solids.addVertices(v8, v9, v10)
				solids.addVertices(v9, v11, v10)
				solids.addVertices(v10, v11, v1)
				solids.addVertices(v11, v0, v1)
				solids.addVertices(v1, v4, v10)
				solids.addVertices(v4, v7, v10)
				solids.closePrimitive()
				
			def plainWall(v0, v1, v2, v3, v4): # Adds a plain, flat, wall. v0 being the lowest left, anti-clockwise
				solids.addVertices(v0, v1, v4) # Triangle, the furthest 'left' of the wall
				solids.addVertices(v1, v3, v4) # Middle triangle
				solids.addVertices(v1, v2, v3) # Right Triangle
				solids.closePrimitive()
			
			def cornerOut(v0, v1, v2, v3, v4, v5): # v0 is the top, v1 is TL, v2 CL, v3 BL, v4 CB, v5 BR
				solids.addVertices(v0, v1, v2)
				solids.addVertices(v0, v2, v3)
				solids.addVertices(v0, v3, v4)
				solids.addVertices(v0, v4, v5)
				solids.closePrimitive()
				
			if ((around[0] == 1) and (around[1] == 0) and (around[2] == 1) and (around[3] == 1)): # Slanting to the left (looking from the 'bottom' of the map upwards)
				plainWall(9, 11, 0, 4, 7)
				
			elif ((around[0] == 1) and (around[1] == 1) and (around[2] == 1) and (around[3] == 0)): # Slanting to the right
				plainWall(3, 5, 6, 10, 1)
				
			elif ((around[0] == 1) and (around[1] == 1) and (around[2] == 0) and (around[3] == 1)): # Slanting downwards
				plainWall(0, 2, 3, 7, 10)
				
			elif ((around[0] == 0) and (around[1] == 1) and (around[2] == 1) and (around[3] == 1)): # Slanting upwards
				plainWall(6, 8, 9, 1, 4)
				
			elif ((around[0] == 1) and (around[1] == 0) and (around[2] == 0) and (around[3] == 1)): # Corner, if Above and Left
				cornerOut(7, 9, 11, 0, 2, 3)
			
			elif ((around[0] == 1) and (around[1] == 1) and (around[2] == 0) and (around[3] == 0)): # Corner, if Above and Right
				cornerOut(10, 0, 2, 3, 5, 6)
				
			elif ((around[0] == 0) and (around[1] == 1) and (around[2] == 1) and (around[3] == 0)): # Corner, if Below and Left
				cornerOut(1, 3, 5, 6, 8, 9)
				
			elif ((around[0] == 0) and (around[1] == 0) and (around[2] == 1) and (around[3] == 1)): # Corner, if Below and Right
				cornerOut(4, 6, 8, 9, 11, 0)
			#addSolid2(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
		
		triData = list[number]
		
		centre = triData[0] # Getting the height data out of the list
		bottomLeft = triData[1]
		bottomCentre = triData[2]
		bottomRight = triData[3]
		rightCentre = triData[4]
		topRight = triData[5]
		topCentre = triData[6]
		topLeft = triData[7]
		leftCentre = triData[8]
		
		vertices.addData3f(0, 0, centre/2) # 0 vertices ## This bit is adding the vertices to make triangles out of
		texcoord.addData2f(0.5,0.5) # And the UV coords
		vertices.addData3f(-size, -size, bottomLeft/2) # 1st
		texcoord.addData2f(0,0)
		vertices.addData3f(0, -size, bottomCentre/2) # 2nd
		texcoord.addData2f(0.5,0)
		vertices.addData3f(size, -size, bottomRight/2) # 3rd
		texcoord.addData2f(1,0)
		vertices.addData3f(size, 0, rightCentre/2) # 4th
		texcoord.addData2f(1,0.5)
		vertices.addData3f(size, size, topRight/2) # 5th
		texcoord.addData2f(1,1)
		vertices.addData3f(0, size, topCentre/2) # 6th
		texcoord.addData2f(0.5,1)
		vertices.addData3f(-size, +size, topLeft/2) # 7th
		texcoord.addData2f(0,1)
		vertices.addData3f(-size, 0, leftCentre/2) # 8th
		texcoord.addData2f(0,0.5)
		
		addTile(0, 1, 2, 3, 4, 5, 6, 7, 8) # Calls the task to make a tile
		
		if tile.solid == True:
			addSolid(size, tile, around)
			geom = Geom(data) 
			geom.addPrimitive(solids) 
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
		plight.setColor(VBase4(1.0,1.0,1.0,1))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)
