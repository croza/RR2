from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import AmbientLight, DirectionalLight, VBase4, VBase3, TextNode
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import *

import modelLoader
import unitHandler

import copy
import random
import sys

def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1), font = loader.loadFont("cmss12"),
                        pos=(-1.3, pos), align=TextNode.ALeft, scale = .1)

class world(DirectObject):
	def __init__(self, parserClass, mapLoaderClass, modelLoaderClass):
		self.loadLight()
		
		self.accept("escape", sys.exit)
		self.accept("s", self.randomChange, [parserClass, mapLoaderClass, modelLoaderClass])
		
		print 'END OF GAMEMAIN.PY!'
		
	def randomChange(self, parserClass, mapLoaderClass, modelLoaderClass):
		x = random.randint(0,9)
		y = random.randint(0,9)

#		mapLoaderClass.tileArray[y][x] = modelLoaderClass.remakeModel(mapLoaderClass.tileArray[x][y],
#																mapLoaderClass,
#																parserClass,
#															#	modelLoaderClass,
#																random.randint(0, 11))

		mapLoaderClass.tileArray[y][x] = self.changeTile(mapLoaderClass.tileArray[y][x], random.randint(0,11), parserClass, modelLoaderClass, mapLoaderClass)
		
	def changeTile(self, firstTile, finalTileNumber, parserClass, modelLoaderClass, mapLoaderClass):
		firstTile.model.detachNode()
		
		posX = firstTile.posX # Setting up values to be transferred to the next tile
		posY = firstTile.posY
		posZ = firstTile.posZ
		cornerMap = firstTile.cornerMap
		solidMap = firstTile.solidMap
		
		finalTileData = parserClass.wall[parserClass.main['wall_types'][finalTileNumber]]
		print finalTileData.fullName
		
		if (finalTileData.solid == False):
			solidMap[4] == False
		
		finalTile = copy.copy(finalTileData)
		finalTile.posX = posX
		finalTile.posY = posY
		finalTile.posZ = posZ
		finalTile.cornerMap = cornerMap
		finalTile.solidMap = solidMap
		
		finalTile.model = modelLoaderClass.makeModel(finalTile)#, mapLoaderClass) # From here on is reparenting and positioning the tile to the right place
#		modelLoaderClass.remakeModel(finalTile, mapLoaderClass)
		finalTile.model.reparentTo(render)
		finalTile.model.setPos(finalTile.posX,finalTile.posY,0)
	
		tex=loader.loadTexture(finalTile.texture)
		finalTile.model.setTexture(tex, 1)
		
		return finalTile
		
	def loadLight(self): #Sets the lights
		plight = AmbientLight('my plight')
		plight.setColor(VBase4(1.0,1.0,1.0,0.5))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)