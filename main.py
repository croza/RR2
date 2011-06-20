from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import AmbientLight, DirectionalLight
from pandac.PandaModules import VBase4, VBase3, TextNode
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText

import modelLoader

import copy
import random
import sys

font = loader.loadFont("cmss12")
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1), font = font,
                        pos=(-1.3, pos), align=TextNode.ALeft, scale = .1)

class world(DirectObject):
	def __init__(self, list, wallClasses):
		self.wallClasses = wallClasses
		self.list = modelLoader.modelLoader().runOnceLoadModels(list)
		
		self.loadLight()
		
		self.accept("escape", sys.exit)
		self.accept("s", self.randomChange)
		
		self.inst1 = addInstructions(0.9, "Press S to randomly change a tile")
		
		print 'END OF MAIN!'
		
	def randomChange(self):
		x = random.randint(0,9)
		y = random.randint(0,9)
		
		self.list[x][y] = self.changeTile(self.list[x][y], self.wallClasses[random.randint(0,11)])
		
	def changeTile(self, firstTile, finalTile):
		firstTile.model.remove()
		posX = firstTile.posX # Setting up values to be transferred to the next tile
		posY = firstTile.posY
		posZ = firstTile.posZ
		
		firstTile = copy.copy(finalTile)
		firstTile.posX = posX
		firstTile.posY = posY
		firstTile.posZ = posZ
		
		firstTile.model = modelLoader.modelLoader().makeModel(firstTile) # From here on is reparenting and positioning the tile to the right place
		firstTile.model.reparentTo(render)
		firstTile.model.setPos(firstTile.posX,firstTile.posY,firstTile.posZ)
		
		tex=loader.loadTexture(firstTile.texture)
		firstTile.model.setTexture(tex, 1)
		
		return firstTile
			
	def loadLight(self): #Sets the lights
		plight = AmbientLight('my plight')
		plight.setColor(VBase4(1.0,1.0,1.0,0.5))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)