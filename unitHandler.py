from pandac.PandaModules import *
#from direct.gui.OnscreenText import OnscreenText
#from direct.actor.Actor import Actor
from direct.task.Task import Task
#from direct.showbase.DirectObject import DirectObject
from panda3d.ai import *

import copy

import astar

class world:
	def __init__(self, parserClass, mapLoaderClass, mainClass):
		self.AIWorld = AIWorld(render)
		
		self.unitDict = parserClass.unit
		self.main = parserClass.main # To redirect the unitID to the unitName
		
		self.gameUnits = {} # A dictionary containing the info of all the in-game units, each with a unique ID as a key
		self.moving = []
		self.unitUniqueID = 0
		
		self.meshes = mainClass.grids
		
		base.cTrav2 = CollisionTraverser('world2')
	#	base.cTrav2.showCollisions(render)
#		self.cTrav = CollisionTraverser('world2')
#		self.cTrav.showCollisions(render)
		
		taskMgr.add(self.tskWorld, 'world update')
		
		
	def addUnit(self, unitID, position, mapLoaderClass):
		self.gameUnits[self.unitUniqueID] = copy.copy(self.unitDict[self.main['units'][unitID]])
		self.gameUnits[self.unitUniqueID].uID = self.unitUniqueID
		self.gameUnits[self.unitUniqueID].modelNode = loader.loadModel(self.gameUnits[self.unitUniqueID].model)
		self.gameUnits[self.unitUniqueID].modelNode.setName('unit')
		self.gameUnits[self.unitUniqueID].modelNode.reparentTo(render)
		self.gameUnits[self.unitUniqueID].modelNode.setPos(position)
		self.gameUnits[self.unitUniqueID].modelNode.setCollideMask(BitMask32.bit(1))

		
		self.gameUnits[self.unitUniqueID].groundRay = CollisionRay()
		self.gameUnits[self.unitUniqueID].groundRay.setOrigin(0,0,1000)
		self.gameUnits[self.unitUniqueID].groundRay.setDirection(0,0,-1)
		
		self.gameUnits[self.unitUniqueID].groundCol = CollisionNode('unit Ray')
		self.gameUnits[self.unitUniqueID].groundCol.addSolid(self.gameUnits[self.unitUniqueID].groundRay)
		self.gameUnits[self.unitUniqueID].groundCol.setTag('units','ray1')
		
		self.gameUnits[self.unitUniqueID].groundCol.setFromCollideMask(BitMask32.bit(0))
	#	self.gameUnits[self.unitUniqueID].groundCol.setIntoCollideMask(BitMask32.allOff())
		self.gameUnits[self.unitUniqueID].groundColNp = self.gameUnits[self.unitUniqueID].modelNode.attachNewNode(self.gameUnits[self.unitUniqueID].groundCol)
		self.gameUnits[self.unitUniqueID].groundHandler = CollisionHandlerFloor()
		self.gameUnits[self.unitUniqueID].groundHandler.setMaxVelocity(9.81)
		
		base.cTrav2.addCollider(self.gameUnits[self.unitUniqueID].groundColNp, self.gameUnits[self.unitUniqueID].groundHandler)

		self.gameUnits[self.unitUniqueID].groundHandler.addCollider(self.gameUnits[self.unitUniqueID].groundColNp, self.gameUnits[self.unitUniqueID].modelNode)
		
#		self.cTrav.addCollider(self.gameUnits[self.unitUniqueID].groundColNp, self.gameUnits[self.unitUniqueID].groundHandler)
		
		self.gameUnits[self.unitUniqueID].groundColNp.show()
		
		self.gameUnits[self.unitUniqueID].AI = AICharacter(self.gameUnits[self.unitUniqueID].fullName,
																self.gameUnits[self.unitUniqueID].modelNode,
																self.gameUnits[self.unitUniqueID].mass*2,
																self.gameUnits[self.unitUniqueID].startForce*2,
																self.gameUnits[self.unitUniqueID].maxForce*2)
		self.AIWorld.addAiChar(self.gameUnits[self.unitUniqueID].AI)
		self.gameUnits[self.unitUniqueID].AIBehaviors = self.gameUnits[self.unitUniqueID].AI.getAiBehaviors()
		self.gameUnits[self.unitUniqueID].moving = False
		
		if (self.gameUnits[self.unitUniqueID].moveType == 'ground'):
			self.gameUnits[self.unitUniqueID].aStar = astar.aStar(self.meshes.landMesh, mapLoaderClass)
		elif (self.gameUnits[self.unitUniqueID].moveType == 'water'):
			self.gameUnits[self.unitUniqueID].aStar = astar.aStar(self.meshes.waterMesh, mapLoaderClass)
		elif (self.gameUnits[self.unitUniqueID].moveType == 'air'):
			self.gameUnits[self.unitUniqueID].aStar = astar.aStar(self.meshes.airMesh, mapLoaderClass)
		self.unitUniqueID += 1
		
	def moveTo(self, destination, uID):
		tempDest = self.gameUnits[uID].aStar.moveTo(self.gameUnits[uID].modelNode, destination)
		if (len(tempDest) >= 1):
			self.gameUnits[uID].AIBehaviors.pathFollow(1)
			self.gameUnits[uID].AIBehaviors.addToPath(Vec3(destination[0], destination[1], 2))
			for point in tempDest:
				self.gameUnits[uID].AIBehaviors.addToPath(Vec3(4*point[0]+2, 4*point[1]+2, 3))
	#		self.gameUnits[uID].AIBehaviors.addToPath(self.gameUnits[uID].model.getPos())
			self.moving.append(uID)
			self.gameUnits[uID].AIBehaviors.startFollow()
		
	def tskWorld(self, task):
		self.AIWorld.update()
		base.cTrav2.traverse(render)
		
		for i in self.gameUnits:
			if (self.gameUnits[i].AIBehaviors.behaviorStatus('pathfollow') == 'done'):
				self.gameUnits[i].AIBehaviors.pauseAi("pathfollow")
			elif (self.gameUnits[i].AIBehaviors.behaviorStatus('pathfollow') == 'active'):
				self.gameUnits[i].modelNode.setP(0)
		
#		for i in self.moving:
#			self.gameUnits[i].setH(0)
		
		return Task.cont