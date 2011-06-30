from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import AmbientLight, DirectionalLight
from pandac.PandaModules import VBase4, VBase3, TextNode
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText

import modelLoader
#import unitHandler

import copy
import random
import sys

font = loader.loadFont("cmss12")
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1), font = font,
                        pos=(-1.3, pos), align=TextNode.ALeft, scale = .1)

class world(DirectObject):
	def __init__(self, list, wallClasses, mapX, mapY, unitDict):
		self.wallClasses = wallClasses
		self.list = modelLoader.modelLoader().runOnceLoadModels(list, mapX)
		
		#g = unitHandler.makeAIWorld().AIWorld
		##h = unitHandler.addNewModel().addNewModel(unitDict, 0, (5,5,10), g)
		#h = unitHandler.addNewModel()
		#h.addNewModel(unitDict, 0, (50,50,0), g)
		#self.accept("enter", h.moveTo)
		
		self.loadLight()
		
		self.accept("escape", sys.exit)
		self.accept("s", self.randomChange)
		
		self.inst1 = addInstructions(0.9, "Press S to randomly change a tile")
		
		print 'END OF MAIN!'
		
	def randomChange(self):
		x = random.randint(0,9)
		y = random.randint(0,9)
		
		self.list[y][x] = self.changeTile(self.list[x][y], self.wallClasses[random.randint(0,11)])
		
	def changeTile(self, firstTile, finalTile): # Transferes one tile's data to another sort of tile
		firstTile.model.remove()
		posX = firstTile.posX # Setting up values to be transferred to the next tile
		posY = firstTile.posY
		posZ = firstTile.posZ
		cornerMap = firstTile.cornerMap
		solidMap = firstTile.solidMap
		
		firstTile = copy.copy(finalTile)
		firstTile.posX = posX
		firstTile.posY = posY
		firstTile.posZ = posZ
		firstTile.cornerMap = cornerMap
		firstTile.solidMap = solidMap
		
		firstTile.model = modelLoader.modelLoader().makeModel(firstTile) # From here on is reparenting and positioning the tile to the right place
		firstTile.model.reparentTo(render)
		firstTile.model.setPos(firstTile.posX,firstTile.posY,0)
		
		tex=loader.loadTexture(firstTile.texture)
		firstTile.model.setTexture(tex, 1)
		
		return firstTile
			
	def loadLight(self): #Sets the lights
		plight = AmbientLight('my plight')
		plight.setColor(VBase4(1.0,1.0,1.0,0.5))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)