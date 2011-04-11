import os, sys, math, random

import random
import mapLib
import config
import wallTypes

from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import AmbientLight
from pandac.PandaModules import VBase4
import direct.directbase.DirectStart

from pandac.PandaModules import GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, Geom, GeomNode, NodePath, GeomPoints  # For triangles

class world(DirectObject):
	def __init__(self, filename):
		self.map = mapLib.Map(filename)
		self.loadWorld()
		self.loadLight()
		
	def loadWorld(self):
		self.tiles = []
		self.solidMap = []
		heightMap = self.map.getHeightMap()
		print heightMap
		w = wallTypes.WorldLoader(heightMap, 5).drawStuff(heightMap, 5)
		ttiles = self.map.generate_tile_array() # The 'data' of all the squares in an array
		# print ttiles
		tileNumber = 0
		tex = loader.loadTexture('data/models/world/textures/ground.png')

		for tile in ttiles:
			wallTypes.wallTypes[tile.typeInt].applyCharacteristics(tile)
			
			#tile.model = loader.loadModel(tile.model)
			#tile.model.setPos(tile.x*4, tile.y*4, 0)
			#tile.model.reparentTo(render)
			
			tiles3 = self.loadTriangles(w, tileNumber, 4*tile.x, 4*tile.y)
			tiles3.reparentTo(render)
			tiles3.setTexture(loader.loadTexture(tile.texture), 1)
			self.tiles.append(tile)
			tileNumber += 1
			
		# legohead = loader.loadModel("data/models/units/lowpol-legohead")
		# legohead.setPos(0, 0, 1)
		# legohead.setScale(3)
		# legohead.reparentTo(render) ## Commented for the moving stuff
		
	def loadTriangles(self, list, number, x, y):
		# format = GeomVertexFormat.getV3() 
		format = GeomVertexFormat.getV3n3c4t2()
		data = GeomVertexData("Data", format, Geom.UHStatic) 
		vertices = GeomVertexWriter(data, "vertex") 
		texcoord= GeomVertexWriter(data, 'texcoord')
		size = 2 # Half the size of the square
		
		triangles = GeomTriangles(Geom.UHStatic)
		
		
		def addTile(v0, v1, v2, v3, v4, v5, v6, v7, v8): # v0 should always be the centre of the tile
			triangles.addVertices(v0, v1, v2) # Remember that this works in an anti-clockwise rotation
			triangles.addVertices(v0, v2, v3)
			triangles.addVertices(v0, v3, v4)
			triangles.addVertices(v0, v4, v5)
			triangles.addVertices(v0, v5, v6)
			triangles.addVertices(v0, v6, v7)
			triangles.addVertices(v0, v7, v8)
			triangles.addVertices(v0, v8, v1)
			triangles.closePrimitive()
		
		triData = list[number]
		
		centre = triData[0]
		bottomLeft = triData[1]
		bottomCentre = triData[2]
		bottomRight = triData[3]
		rightCentre = triData[4]
		topRight = triData[5]
		topCentre = triData[6]
		topLeft = triData[7]
		leftCentre = triData[8]
		
		vertices.addData3f(x, y, centre) # 0 vertices
		texcoord.addData2f(0.5,0.5)
		vertices.addData3f(x-size, y-size, bottomLeft) # 1st
		texcoord.addData2f(0,0)
		vertices.addData3f(x, y-size, bottomCentre) # 2nd
		texcoord.addData2f(0.5,0)
		vertices.addData3f(x+size, y-size, bottomRight) # 3rd
		texcoord.addData2f(1,0)
		vertices.addData3f(x+size, y, rightCentre) # 4th
		texcoord.addData2f(1,0.5)
		vertices.addData3f(x+size, y+size, topRight) # 5th
		texcoord.addData2f(1,1)
		vertices.addData3f(x-size, y+size, topCentre) # 6th
		texcoord.addData2f(0.5,1)
		vertices.addData3f(x-size, y, topLeft) # 7th
		texcoord.addData2f(0,1)
		vertices.addData3f(x-size, y, leftCentre) # 8th
		texcoord.addData2f(0,0.5)
		
		addTile(0, 1, 2, 3, 4, 5, 6, 7, 8)
		
		geom = Geom(data) 
		geom.addPrimitive(triangles) 

		node = GeomNode("CubeMaker") 
		node.addGeom(geom)
		
		return NodePath(node) 
		
	def loadLight(self): #Sets the lights
		plight = AmbientLight('my plight')
		plight.setColor(VBase4(1.0,1.0,1.0,1))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)
