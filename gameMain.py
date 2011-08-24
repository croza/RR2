from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import AmbientLight, DirectionalLight, VBase4, VBase3, TextNode, PointLight
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import Task
from pandac.PandaModules import Point2

from direct.interval.IntervalGlobal import *

import Parser
import mapLoader
import modelLoader
import stratCam
import unitHandler
import astar

import copy
import random
import sys
import random

#from direct.gui.OnscreenImage import OnscreenImage
#from direct.actor.Actor import Actor

def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1), font = loader.loadFont("cmss12"),
                        pos=(-1.3, pos), align=TextNode.ALeft, scale = .1)

class world(DirectObject):
	def __init__(self):
		self.parserClass = Parser.Parser() # Making the required instances
		self.mapLoaderClass = mapLoader.mapLoader(self)
		
		self.gameObjects = {}
		self.gameObjectID = 0
		
		self.mapX = self.mapLoaderClass.mapConfigParser.getint("map", "width") - 1 # Name says it all really
		self.mapY = self.mapLoaderClass.mapConfigParser.getint("map", "height") - 1

		self.modelLoaderClass = modelLoader.modelLoader(self)
		self.cameraClass = stratCam.CameraHandler(self)
		
		base.setFrameRateMeter(True)
	
		self.grids = astar.grid(self)
		
		self.unitHandler = unitHandler.world(self)
		self.unitHandler.addUnit(0, (10,10,0), self)
		self.unitHandler.addUnit(0, (6,10,0), self)
		self.unitHandler.moveTo((6, 34), 0)
		self.unitHandler.moveTo((34, 30), 1)
		
		self.tileSelected = (0,0)
		
		taskMgr.add(self.tskCheckWalls, "Wall checking")
		
		self.loadLight()
		
		self.accept("escape", sys.exit)
		
		print 'END OF GAMEMAIN.PY!'
		
	def tskCheckWalls(self, task):
		for row in self.mapLoaderClass.tileArray:
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
					tile.solidMap[7] == False) or#):
					
					(tile.modelName[0:13] == 'solid no work')):
						self.mineWall(tile)
						#self.changeTile(tile, 0, parserClass, modelLoaderClass, mapLoaderClass)
		return Task.cont

	def mineWall(self, firstTile):
		def changer(firstTile, finalTileNumber):
			firstTile.model.detachNode()
			
			finalTileData = self.parserClass.wall[self.parserClass.main['wall_types'][finalTileNumber]]
			
			finalTile = copy.copy(finalTileData)
			finalTile.posX = firstTile.posX
			finalTile.posY = firstTile.posY
			finalTile.posZ = firstTile.posZ
			finalTile.cornerMap = firstTile.cornerMap
			finalTile.solidMap = firstTile.solidMap
			finalTile.reda = 0
			finalTile.renu = 0
			
			print finalTile.posX/4, finalTile.posY/4
			
			if (finalTileData.solid == False):
				finalTile.solidMap[4] == False
				if (finalTile.walkable == True): # Change the meshes for the new tile
					self.grids.landMesh[finalTile.posY/4][finalTile.posX/4] = True
				else:
					self.grids.landMesh[finalTile.posY/4][finalTile.posX/4] = False
				if (finalTile.water == True):
					self.grids.waterMesh[finalTile.posY/4][finalTile.posX/4] = True
				else:
					self.grids.waterMesh[finalTile.posY/4][finalTile.posX/4] = False
				if (finalTile.lava == True) or (firstTile.water == True) or (firstTile.walkable == True):
					self.grids.airMesh[finalTile.posY/4][finalTile.posX/4] = True
				else:
					self.grids.airMesh[finalTile.posY/4][finalTile.posX/4] = False
				
			elif (finalTileData.solid == True):
				finalTile.solidMap[4] == True
				
				self.grids.landMesh[finalTile.posY][finalTile.posX] = True
				self.grids.waterMesh[finalTile.posY][finalTile.posX] = False
				self.grids.waterMesh[finalTile.posY][finalTile.posX] = True
			
			finalTile.model = self.modelLoaderClass.makeModel(finalTile)#, mapLoaderClass) # From here on is reparenting and positioning the tile to the right place

			finalTile.model.reparentTo(render)
			finalTile.model.setPos(finalTile.posX, finalTile.posY, 0)
			finalTile.model.setCollideMask(0x1)
			
			tex = loader.loadTexture(finalTile.texture)
			finalTile.model.setTexture(tex, 1)
			
#			if (firstTile.cror % 2 == 1):
#				print str((firstTile.cror + 1)/2)+' energy crystals'
#			else:
#				print str(firstTile.cror / 2)+' ore'
#			
			print self.parserClass.main['objects'][firstTile.reda], firstTile.renu
			
			for i in range(firstTile.renu):
				self.modelLoaderClass.addObject(self, firstTile.reda, finalTile)
#				self.gameObjects[self.gameObjectID] = copy.copy(self.parserClass.object[self.parserClass.mainConfig.get('objects', str(firstTile.reda))])
#				self.gameObjects[self.gameObjectID].modelNode = loader.loadModel(self.gameObjects[self.gameObjectID].model)
#				self.gameObjects[self.gameObjectID].modelNode.setPos(firstTile.posX-2+random.randint(0,3)+random.random(), firstTile.posY-2+random.randint(0,3)+random.random(), 10)
#				self.gameObjects[self.gameObjectID].modelNode.reparentTo(render)
#				self.gameObjects[self.gameObjectID].modelNode.setCollideMask(BitMask32.bit(0))
				
				self.gameObjectID += 1
				
	#		print parserClass.object[parserClass.main['objects'][firstTile.reda]]
			return finalTile
			
		self.mapLoaderClass.tileArray[firstTile.posY/4][firstTile.posX/4] = changer(firstTile, 0)
		self.reloadSurround(self.mapLoaderClass.tileArray[firstTile.posY/4][firstTile.posX/4])

	def reloadSurround(self, tileChanged):
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
			
		aroundInfo.append(self.mapLoaderClass.tileArray[yBehind][xBehind]) # BL
		aroundInfo.append(self.mapLoaderClass.tileArray[yBehind][tileChanged.posX/4]) # BC
		aroundInfo.append(self.mapLoaderClass.tileArray[yBehind][xInfront]) # BR
		
		aroundInfo.append(self.mapLoaderClass.tileArray[tileChanged.posY/4][xBehind]) # L
		aroundInfo.append(self.mapLoaderClass.tileArray[tileChanged.posY/4][tileChanged.posX/4-1])
		aroundInfo.append(self.mapLoaderClass.tileArray[tileChanged.posY/4][xInfront]) # R
		
		aroundInfo.append(self.mapLoaderClass.tileArray[yInfront][xBehind]) # TL
		aroundInfo.append(self.mapLoaderClass.tileArray[yInfront][tileChanged.posX/4]) # TC
		aroundInfo.append(self.mapLoaderClass.tileArray[yInfront][xInfront]) # TR
		
		name  = self.mapLoaderClass.tileArray[tileChanged.posY/4+1][tileChanged.posX/4+1].modelName
		
		for around in aroundInfo:
			around.solidMap = self.modelLoaderClass.reloadSolidMap(self, around.posX/4, around.posY/4)
			
			around.model.remove()
			
			around.model = self.modelLoaderClass.makeModel(around)
			around.model.setCollideMask(0x01)
			
			around.model.reparentTo(render)
			around.model.setPos(around.posX, around.posY, 0)

			tex = loader.loadTexture(around.texture)
			around.model.setTexture(tex, 1)
		
	def loadLight(self): #Sets the lights
		plight = AmbientLight('my plight')
		light = self.parserClass.userConfig.getfloat('display', 'light')
		plight.setColor(VBase4(light,light,light,0.5))
#		plight.setColor(VBase4(0.5,0.5,0.5,0.5))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)
		
w = world()
run()