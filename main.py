import os, sys, math, random

import random
import mapLib
import config
import wallTypes

from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import AmbientLight
from pandac.PandaModules import VBase4
import direct.directbase.DirectStart


class world(DirectObject):
	def __init__(self, filename):
		self.map = mapLib.Map(filename)
		self.loadWorld()
		self.loadLight()
		
	def loadWorld(self):
		self.tiles = []
		ttiles = self.map.generate_tile_array()
		for tile in ttiles:
			wallTypes.wallTypes[tile.typeInt].applyCharacteristics(tile)
			tile.model = loader.loadModel(tile.model)
			tile.model.setPos(tile.x*4, tile.y*4, 0)
			tile.model.reparentTo(render)
			self.tiles.append(tile)
		legohead = loader.loadModel("data/models/units/lowpol-legohead")
		legohead.setPos(0, 0, 1)
		legohead.reparentTo(render)
		
	def loadLight(self): #Sets the lights
		plight = AmbientLight('my plight')
		plight.setColor(VBase4(1.0,1.0,1.0,1))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)
