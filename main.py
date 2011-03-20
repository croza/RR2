import os, sys, math, random

from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.task import *
from direct.actor.Actor import Actor
from panda3d.ai import *
from direct.gui.OnscreenText import OnscreenText


import random
import mapLib
import config
import wallTypes

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
		
	def loadLight(self): #Sets the lights
		plight = AmbientLight('my plight')
		plight.setColor(VBase4(1.0,1.0,1.0,1))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)
