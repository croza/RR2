from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import AmbientLight, DirectionalLight, VBase4, VBase3, TextNode
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import Task

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
		taskMgr.add(self.tskCheckWalls, "Wall checking", extraArgs = [mapLoaderClass, parserClass, modelLoaderClass])
		
		self.loadLight()
		
		self.mapX = mapLoaderClass.mapConfigParser.getint("map", "width")
		self.mapY = mapLoaderClass.mapConfigParser.getint("map", "height")
		
		self.accept("escape", sys.exit)
		self.accept("s", self.randomChange, [parserClass, mapLoaderClass, modelLoaderClass])
		
		print 'END OF GAMEMAIN.PY!'
		
	def tskCheckWalls(self, mapLoaderClass, parserClass, modelLoaderClass):
		for row in mapLoaderClass.tileArray:
			for tile in row:
				if (tile.solid == True):
					if ((tile.solidMap[1] == True and
					tile.solidMap[3] == False and
					tile.solidMap[5] == False and
					tile.solidMap[7] == False) or
					
					(tile.solidMap[1] == False and
					tile.solidMap[3] == True and
					tile.solidMap[5] == False and
					tile.solidMap[7] == False) or
					
					(tile.solidMap[1] == False and
					tile.solidMap[3] == False and
					tile.solidMap[5] == True and
					tile.solidMap[7] == False) or
					
					(tile.solidMap[1] == False and
					tile.solidMap[3] == False and
					tile.solidMap[5] == False and
					tile.solidMap[7] == True) or
					
					(tile.solidMap[1] == True and
					tile.solidMap[3] == False and
					tile.solidMap[5] == False and
					tile.solidMap[7] == True) or
					
					(tile.solidMap[1] == False and
					tile.solidMap[3] == True and
					tile.solidMap[5] == True and
					tile.solidMap[7] == False)):
						self.changeTile(tile, 0, parserClass, modelLoaderClass, mapLoaderClass)
						
		return Task.cont
		
	def randomChange(self, parserClass, mapLoaderClass, modelLoaderClass):
		x = random.randint(3,7)
		y = random.randint(3,7)

		self.changeTile(mapLoaderClass.tileArray[y][x], random.randint(0,1), parserClass, modelLoaderClass, mapLoaderClass)
		
	def changeTile(self, firstTile, finalTileNumber, parserClass, modelLoaderClass, mapLoaderClass):
		def changer(firstTile, finalTileNumber, parserClass, modelLoaderClass, mapLoaderClass):
			firstTile.model.detachNode()
			
			posX = firstTile.posX # Setting up values to be transferred to the next tile
			posY = firstTile.posY
			posZ = firstTile.posZ
			cornerMap = firstTile.cornerMap
			solidMap = firstTile.solidMap
			
			finalTileData = parserClass.wall[parserClass.main['wall_types'][finalTileNumber]]
			
			if (finalTileData.solid == False):
				solidMap[4] == False
				
			elif (finalTileData.solid == True):
				solidMap[4] == True
			
			finalTile = copy.copy(finalTileData)
			finalTile.posX = posX
			finalTile.posY = posY
			finalTile.posZ = posZ
			finalTile.cornerMap = cornerMap
			finalTile.solidMap = solidMap
			
			finalTile.model = modelLoaderClass.makeModel(finalTile)#, mapLoaderClass) # From here on is reparenting and positioning the tile to the right place
				
			finalTile.model.reparentTo(render)
			finalTile.model.setPos(finalTile.posX, finalTile.posY, 0)
		
			tex=loader.loadTexture(finalTile.texture)
			finalTile.model.setTexture(tex, 1)
			
			return finalTile
			
		mapLoaderClass.tileArray[firstTile.posY/4][firstTile.posX/4] = changer(firstTile, finalTileNumber, parserClass, modelLoaderClass, mapLoaderClass)
		self.reloadSurround(mapLoaderClass.tileArray[firstTile.posY/4][firstTile.posX/4], mapLoaderClass, modelLoaderClass, parserClass)
		
	def reloadSurround(self, tileChanged, mapLoaderClass, modelLoaderClass, parserClass):
		aroundInfo = []
		
		yBehind = tileChanged.posY/4 - 1
		yInfront = tileChanged.posY/4 +1
		
		xBehind = tileChanged.posX/4 - 1
		xInfront = tileChanged.posX/4 + 1
		
		if (yInfront >= self.mapY-1):
			yInfront = self.mapY-1
			
		if (yBehind <= 0):
			yBehind = 0
			
		if (xInfront >= self.mapX-1):
			xInfront = self.mapX-1
			
		if (xBehind <= 0):
			xBehind = 0
			
		aroundInfo.append(mapLoaderClass.tileArray[yBehind][xBehind]) # BL
		aroundInfo.append(mapLoaderClass.tileArray[yBehind][tileChanged.posX/4]) # BC
		aroundInfo.append(mapLoaderClass.tileArray[yBehind][xInfront]) # BR
		
		aroundInfo.append(mapLoaderClass.tileArray[tileChanged.posY/4][xBehind]) # L
		aroundInfo.append(mapLoaderClass.tileArray[tileChanged.posY/4][tileChanged.posX/4-1])
		aroundInfo.append(mapLoaderClass.tileArray[tileChanged.posY/4][xInfront]) # R
		
		aroundInfo.append(mapLoaderClass.tileArray[yInfront][xBehind]) # TL
		aroundInfo.append(mapLoaderClass.tileArray[yInfront][tileChanged.posX/4]) # TC
		aroundInfo.append(mapLoaderClass.tileArray[yInfront][xInfront]) # TR
		
		name  = mapLoaderClass.tileArray[tileChanged.posY/4+1][tileChanged.posX/4+1].modelName
		
		for around in aroundInfo:
			around.solidMap = modelLoaderClass.reloadSolidMap(mapLoaderClass, around.posX/4, around.posY/4)
			
			around.model.remove()
			
			around.model = modelLoaderClass.makeModel(around)
			around.model.setCollideMask(0x01)
			
			around.model.reparentTo(render)
			around.model.setPos(around.posX, around.posY, 0)
			
			tex = loader.loadTexture(around.texture)
			around.model.setTexture(tex, 1)
		
	def loadLight(self): #Sets the lights
		plight = AmbientLight('my plight')
		plight.setColor(VBase4(1.0,1.0,1.0,0.5))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)