from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import AmbientLight, DirectionalLight, VBase4, VBase3, TextNode, PointLight
from panda3d.core import Fog
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import Task
from pandac.PandaModules import Point2, RigidBodyCombiner, NodePath, CollisionNode, CollisionRay, BitMask32, CollisionHandlerQueue, CollisionTraverser

from direct.gui.DirectGui import DirectFrame, DirectButton

from direct.interval.IntervalGlobal import *

import Parser
import mapLoader
import modelLoader
import stratCam
import unitHandler
import astar
import buildingHandler
import priorities

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
		base.disableMouse()
		base.camLens.setFar(100)
		self.parserClass = Parser.Parser() # Making the required instances
		self.mapLoaderClass = mapLoader.mapLoader(self)
		
		self.gameObjects = {}
		self.gameObjectID = 0
		
		self.mapX = self.mapLoaderClass.mapConfigParser.getint("map", "width") - 1 # Name says it all really
		self.mapY = self.mapLoaderClass.mapConfigParser.getint("map", "height") - 1

		self.modelLoaderClass = modelLoader.modelLoader(self)
		
		
		self.cameraClass = stratCam.CameraHandler(self)
		self.mouseClass = stratCam.mouseHandler(self)
		self.GUI = stratCam.GUI(self)
	#	self.GUI = stratCam.GUI(self)
		self.priorities = priorities.priorities()
		
		base.setFrameRateMeter(True)
		
		###############
		base.cTrav2 = CollisionTraverser('world2')
	#	base.cTrav2.showCollisions(render)
		
		self.heightRay = CollisionRay() # A collision ray, used for getting the height of the terrain
		self.heightRay.setOrigin(0,0,100)
		self.heightRay.setDirection(0,0,-1)
		
		self.heightCol = CollisionNode('unit Ray')
		self.heightCol.addSolid(self.heightRay)
		self.heightCol.setTag('units','ray1')
		
		self.heightCol.setFromCollideMask(BitMask32.bit(0))
	#	self.heightCol.setIntoCollideMask(BitMask32.allOff())
		self.heightColNp = render.attachNewNode(self.heightCol)
		self.heightColNp.setPos(2,2,0)
		self.heightHandler = CollisionHandlerQueue()
		
		base.cTrav2.addCollider(self.heightColNp, self.heightHandler)
		###############
		
	#	myFrame = DirectFrame(frameColor=(0, 0, 0, 1),
	#					frameSize=(-0.25, 0.25, -1, 1),
	#					pos=(1.08, 0, 0))
	#	button = DirectButton(text = ("button"), scale = 0.1)
	#	button.reparentTo(myFrame)
	#	button.setPos(0, 0, 0.9)
		
		self.grids = astar.grid(self)
		
		self.unitHandler = unitHandler.world(self)
	#	self.unitHandler.addUnit(0, (10,10,5), self)
	#	self.unitHandler.addUnit(1, (6,10,5), self)
	#	self.unitHandler.moveTo(self, (6, 34), 0)
	#	self.unitHandler.moveTo(self, (34, 30), 1)
		
		
		
		self.buildingHandler = buildingHandler.buildingHandler(self)
		
		self.tileSelected = (0,0)
		
		taskMgr.add(self.tskCheckWalls, "Wall checking")
		taskMgr.add(self.priorities.jobTask, "Jobs", extraArgs = [self])
		
		self.loadLight()
		
		self.accept("escape", sys.exit)
		self.accept("1", self.unitHandler.addUnit2, extraArgs = [0, self])
		self.accept("2", self.unitHandler.addUnit2, extraArgs = [1, self])
		self.accept("3", self.unitHandler.addUnit2, extraArgs = [2, self])
		
		self.accept("enter", self.buildingHandler.addBuilding2, extraArgs = [self, 0])
		
		self.accept("p", self.priorities.addJob)
		
		print 'END OF GAMEMAIN.PY!'
		
	def tskCheckWalls(self, task):
		for row in self.mapLoaderClass.tileArray:
			for tile in row:
				if (tile.solid == True):
					aroundNo = 0
				#	if (tile.solidMap[1] == True):
				#		aroundNo += 1
				#	if (tile.solidMap[3] == True):
				#		aroundNo += 1
				#	if (tile.solidMap[5] == True):
				#		aroundNo += 1
				#	if (tile.solidMap[7] == True):
				#		aroundNo += 1
					for i in tile.solidMap:
						if (i == True):
							aroundNo += 1
					
					if ((tile.solidMap[1] == True and # If only supported by 1 other solid
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
					
					(aroundNo < 3)):
					
					#(tile.modelName[0:13] == 'solid no work')):
						self.mineWall(tile)
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
					
				if (finalTile.lava == True) or (finalTile.water == True) or (finalTile.walkable == True):
					self.grids.airMesh[finalTile.posY/4][finalTile.posX/4] = True
				else:
					self.grids.airMesh[finalTile.posY/4][finalTile.posX/4] = False
				
			elif (finalTileData.solid == True):
				finalTile.solidMap[4] == True
				
				self.grids.landMesh[finalTile.posY/4][finalTile.posX/4] = True
				self.grids.waterMesh[finalTile.posY/4][finalTile.posX/4] = True
				self.grids.airMesh[finalTile.posY/4][finalTile.posX/4] = True
			
			finalTile.model = self.modelLoaderClass.makeModel(finalTile, self)#, mapLoaderClass) # From here on is reparenting and positioning the tile to the right place

			finalTile.model.reparentTo(render)
			finalTile.model.setPos(finalTile.posX, finalTile.posY, 0)
			finalTile.model.setCollideMask(0x1)
			
			tex = loader.loadTexture(finalTile.texture)
			finalTile.model.setTexture(tex, 1)
			
			if (firstTile.renu != 0):
				print self.parserClass.main['objects'][firstTile.reda], firstTile.renu
			
				for i in range(firstTile.renu):
					self.modelLoaderClass.addObject(self, firstTile.reda, finalTile)
				
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
			
			around.model = self.modelLoaderClass.makeModel(around, self)
			around.model.setCollideMask(0x01)
			
			around.model.reparentTo(render)
			around.model.setPos(around.posX, around.posY, 0)

			tex = loader.loadTexture(around.texture)
			around.model.setTexture(tex, 1)
		
	def loadLight(self): #Sets the lights
		plight = AmbientLight('my plight')
		light = self.parserClass.userConfig.getfloat('display', 'light')
		plight.setColor(VBase4(light,light,light,0.5))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)

w = world()
addInstructions(-0.9, "1-3 add units at the mouse click")
run()