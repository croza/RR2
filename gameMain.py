from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import AmbientLight, DirectionalLight, VBase4, VBase3, TextNode
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import Task
from pandac.PandaModules import Point2
from pandac.PandaModules import CollisionHandlerEvent, CollisionNode, CollisionSphere, CollisionTraverser, BitMask32, CollisionRay, CollisionHandlerQueue

from direct.interval.IntervalGlobal import *

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
		self.tileSelected = (0,0)
		
		taskMgr.add(self.tskCheckWalls, "Wall checking", extraArgs = [mapLoaderClass, parserClass, modelLoaderClass])
		
		self.loadLight()
		
		self.mapX = mapLoaderClass.mapConfigParser.getint("map", "width")
		self.mapY = mapLoaderClass.mapConfigParser.getint("map", "height")
		
		self.accept("escape", sys.exit)
		self.accept("s", self.randomChange, [parserClass, mapLoaderClass, modelLoaderClass])
		self.accept("mouse1", self.mouseClick, [mapLoaderClass])
		self.accept("q", self.changeTile, [mapLoaderClass.tileArray[self.tileSelected[1]][self.tileSelected[0]], 0, parserClass, modelLoaderClass, mapLoaderClass])
		
		print 'END OF GAMEMAIN.PY!'
		
		###############################################
		
		
		
		#** Collision events ignition
		base.cTrav = CollisionTraverser()
		collisionHandler = CollisionHandlerEvent()
		self.collisionHandler2 = CollisionHandlerQueue()

		#** Setting the ray collider - see step5.py for details
		pickerNode=CollisionNode('mouseraycnode')
		
		pickerNP=base.camera.attachNewNode(pickerNode)
		
		self.pickerRay=CollisionRay()
		pickerNode.addSolid(self.pickerRay)
		
		base.cTrav.showCollisions(render)

		#** This is new stuff: we set here a so called 'tag' for the ray - its purpose is to make the ray recognizable in a different event pattern matching situation from what we are used to use so far. Just note the first parameter is the main object grouping. See details below setting the patterns.
		pickerNode.setTag('rays','ray1')
		base.cTrav.addCollider(pickerNP, self.collisionHandler2)
		
		taskMgr.add(self.rayupdate, "blah")
		
		self.entries = []
	
#	def mouseClick(self, status):
#		if status == 'down':
#			pickingEnabledOject.setScale(.9)
#			snipstuff.info_message("You clicked '%s'!"%pickingEnabledOject.getName())

#		if status == 'up':
#			pickingEnabledOject.setScale(1.0)
#	def destroyWall(self, firstTile, finalTileNumber, parserClass, modelLoaderClass, mapLoaderClass):
#		if (self.tileSelected != (0,0)):
#			self.changeTile(firstTile, finalTileNumber, parserClass, modelLoaderClass, mapLoaderClass)

	def rayupdate(self, task):
		if base.mouseWatcherNode.hasMouse():
			self.entries = []
			for i in range(self.collisionHandler2.getNumEntries()):
				entry = self.collisionHandler2.getEntry(i)
				self.entries.append(entry)
			self.entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
									 x.getSurfacePoint(render).getZ()))	
			
#			if (len(self.entries)>0):
#				print self.entries[0].getIntoNode().getName()
			
			mpos=base.mouseWatcherNode.getMouse()
			# this function will set our ray to shoot from the actual camera lenses off the 3d scene, passing by the mouse pointer position, making  magically hit what is pointed by it in the 3d space
			self.pickerRay.setFromLens(base.camNode, mpos.getX(),mpos.getY())
		return task.cont
	
	def mouseClick(self, mapLoaderClass):
		if (len(self.entries)>0):
			x = int(self.entries[0].getIntoNode().getName()[len(self.entries[0].getIntoNode().getName())-6:len(self.entries[0].getIntoNode().getName())-4])
			y = int(self.entries[0].getIntoNode().getName()[len(self.entries[0].getIntoNode().getName())-2:])
			

			if (mapLoaderClass.tileArray[y][x].walkable == True) or (mapLoaderClass.tileArray[y][x].drillTime != None):
				print self.tileSelected
				mapLoaderClass.tileArray[self.tileSelected[1]][self.tileSelected[0]].model.setColor(1,1,1,1)
				
				mapLoaderClass.tileArray[y][x].model.setColor(0.5,1,0.5,1)
				self.tileSelected = (x, y)
				
			else:
				self.tileSelected = (0,0)
#		pos = Point2(base.mouseWatcherNode.getMouse()) 
#		pos.setX(pos.getX()*1.33) 
#		
#		p3 = base.cam.getRelativePoint(render, point3d) 
#		
#		print pos, p3
		
		
	###############################################################################
		
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
					tile.solidMap[7] == False) or
					
					(tile.modelName[0:4] == 'none')):
						self.changeTile(tile, 0, parserClass, modelLoaderClass, mapLoaderClass)
		return Task.cont
		
	def randomChange(self, parserClass, mapLoaderClass, modelLoaderClass):
		x = random.randint(1,8)
		y = random.randint(1,8)
		
#		seq = Sequence()
#		seq.append(Func(mapLoaderClass.tileArray[y][x].model.setColor, (0,1,0,1)))
#		seq.append(Wait(1))
#		seq.append(Func(self.changeTile, mapLoaderClass.tileArray[y][x], 1, parserClass, modelLoaderClass, mapLoaderClass))
		
#		seq.start()
		
		mapLoaderClass.tileArray[y][x] = self.changeTile(mapLoaderClass.tileArray[y][x], random.randint(0,1), parserClass, modelLoaderClass, mapLoaderClass)
		
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
			finalTile.model.setCollideMask(0x1)
			
			tex = loader.loadTexture(finalTile.texture)
			finalTile.model.setTexture(tex, 1)
			
			print finalTile.solid
			return finalTile
			
		mapLoaderClass.tileArray[firstTile.posY/4][firstTile.posX/4] = changer(firstTile, finalTileNumber, parserClass, modelLoaderClass, mapLoaderClass)
		self.reloadSurround(mapLoaderClass.tileArray[firstTile.posY/4][firstTile.posX/4], mapLoaderClass, modelLoaderClass, parserClass)
		
	def mineWall(self, unitNumber, firstTile, parserClass, modelLoaderClass, mapLoaderClass):
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
			finalTile.model.setCollideMask(0x1)
			
			tex = loader.loadTexture(finalTile.texture)
			finalTile.model.setTexture(tex, 1)
			
			
			return finalTile
			
		mapLoaderClass.tileArray[firstTile.posY/4][firstTile.posX/4] = changer(firstTile, 0, parserClass, modelLoaderClass, mapLoaderClass)
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