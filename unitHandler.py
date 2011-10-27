from pandac.PandaModules import *
#from direct.gui.OnscreenText import OnscreenText
#from direct.actor.Actor import Actor
from direct.task.Task import Task
#from direct.showbase.DirectObject import DirectObject
from panda3d.ai import *
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib

import copy

import astar

class world:
	def __init__(self, mainClass):
		self.AIWorld = AIWorld(render)
		
		self.unitDict = mainClass.parserClass.unit
		print self.unitDict
		self.main = mainClass.parserClass.main # To redirect the unitID to the unitName
		
		self.gameUnits = {} # A dictionary containing the info of all the in-game units, each with a unique ID as a key
		self.unitUniqueID = 0
		
		self.meshes = mainClass.grids
		
		taskMgr.add(self.tskWorld, 'world update')
		
	def addUnit2(self, unitID, mainClass):
		self.addUnit(unitID, mainClass.mouseClass.getMousePos(), mainClass)
		
	def addUnit(self, unitID, position, mainClass):
		self.gameUnits[self.unitUniqueID] = Unit(unitID, position, mainClass)
		self.unitUniqueID += 1
		#print self.gameUnits,self.gameUnits[self.unitUniqueID]
		
	def addUnit_temp(self, unitID, position, mainClass):
		self.gameUnits[self.unitUniqueID] = copy.copy(self.unitDict[self.main['units'][unitID]])
		self.gameUnits[self.unitUniqueID].uID = self.unitUniqueID
		self.gameUnits[self.unitUniqueID].modelNode = loader.loadModel(self.gameUnits[self.unitUniqueID].model)
		self.gameUnits[self.unitUniqueID].modelNode.setName('unit ' + str(self.unitUniqueID).zfill(3))
		self.gameUnits[self.unitUniqueID].modelNode.reparentTo(render)
		self.gameUnits[self.unitUniqueID].modelNode.setPos(position)
		self.gameUnits[self.unitUniqueID].modelNode.setCollideMask(BitMask32.bit(1))
		
		self.gameUnits[self.unitUniqueID].select = OnscreenImage(image = 'data/models/game/selected.png')
		self.gameUnits[self.unitUniqueID].select.setScale(float(self.gameUnits[self.unitUniqueID].selectScale))
		self.gameUnits[self.unitUniqueID].select.reparentTo(self.gameUnits[self.unitUniqueID].modelNode)
		self.gameUnits[self.unitUniqueID].select.setZ(float(self.gameUnits[self.unitUniqueID].modelHeight)/2)
		self.gameUnits[self.unitUniqueID].select.setTransparency(TransparencyAttrib.MAlpha)
		self.gameUnits[self.unitUniqueID].select.setBillboardPointEye()
		self.gameUnits[self.unitUniqueID].select.hide()
		
		self.gameUnits[self.unitUniqueID].groundRay = CollisionRay()
		self.gameUnits[self.unitUniqueID].groundRay.setOrigin(0,0,100)
		self.gameUnits[self.unitUniqueID].groundRay.setDirection(0,0,-1)
		
		self.gameUnits[self.unitUniqueID].groundCol = CollisionNode('unit Ray')
		self.gameUnits[self.unitUniqueID].groundCol.addSolid(self.gameUnits[self.unitUniqueID].groundRay)
		self.gameUnits[self.unitUniqueID].groundCol.setTag('units','ray1')
		
		self.gameUnits[self.unitUniqueID].groundCol.setFromCollideMask(BitMask32.bit(0))
	#	self.gameUnits[self.unitUniqueID].groundCol.setIntoCollideMask(BitMask32.allOff())
		self.gameUnits[self.unitUniqueID].groundColNp = self.gameUnits[self.unitUniqueID].modelNode.attachNewNode(self.gameUnits[self.unitUniqueID].groundCol)
		self.gameUnits[self.unitUniqueID].groundColNp.setPos(0,0,0)
		self.gameUnits[self.unitUniqueID].groundHandler = CollisionHandlerFloor()
		self.gameUnits[self.unitUniqueID].groundHandler.setMaxVelocity(100)
		
		base.cTrav2.addCollider(self.gameUnits[self.unitUniqueID].groundColNp, self.gameUnits[self.unitUniqueID].groundHandler)

		self.gameUnits[self.unitUniqueID].groundHandler.addCollider(self.gameUnits[self.unitUniqueID].groundColNp, self.gameUnits[self.unitUniqueID].modelNode)
		
		self.gameUnits[self.unitUniqueID].AI = AICharacter(self.gameUnits[self.unitUniqueID].fullName,
																self.gameUnits[self.unitUniqueID].modelNode,
																self.gameUnits[self.unitUniqueID].mass*2,
																self.gameUnits[self.unitUniqueID].startForce*2,
																self.gameUnits[self.unitUniqueID].maxForce*2)
		self.AIWorld.addAiChar(self.gameUnits[self.unitUniqueID].AI)
		self.gameUnits[self.unitUniqueID].AIBehaviors = self.gameUnits[self.unitUniqueID].AI.getAiBehaviors()
		
		if (self.gameUnits[self.unitUniqueID].moveType == 'ground'):
			self.gameUnits[self.unitUniqueID].aStar = astar.aStar(self.meshes.landMesh, mainClass)
		elif (self.gameUnits[self.unitUniqueID].moveType == 'water'):
			self.gameUnits[self.unitUniqueID].aStar = astar.aStar(self.meshes.waterMesh, mainClass)
		elif (self.gameUnits[self.unitUniqueID].moveType == 'air'):
			self.gameUnits[self.unitUniqueID].aStar = astar.aStar(self.meshes.airMesh, mainClass)

		self.unitUniqueID += 1
		
	def moveTo(self, mainClass, destination, uID, userJob = False): # Movees the unit
		def getHeight(position, mainClass):
			mainClass.heightColNp.setPos(position[0], position[1], 100)
			base.cTrav2.traverse(render)
			
			entries = []
			for i in range(mainClass.heightHandler.getNumEntries()):
				entry = mainClass.heightHandler.getEntry(i)
				entries.append(entry)
			entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
										 x.getSurfacePoint(render).getZ()))	
			
			if (len(entries)>0):
				return entries[0].getSurfacePoint(render).getZ()
			else:
				return 3
		
	#	print self.gameUnits[uID].modelNode.getPos()
		if (userJob == True):
			self.gameUnits[uID].job = ["moving",destination]
			taskMgr.add(self.tskMove, "Moving task", extraArgs = [uID])
			
		tempDest = self.gameUnits[uID].aStar.moveTo(self.gameUnits[uID].modelNode, destination)
		if (len(tempDest) >= 1):
			self.gameUnits[uID].AIBehaviors.pathFollow(1)
			
			self.gameUnits[uID].AIBehaviors.addToPath(Vec3(destination[0], destination[1], getHeight(destination, mainClass)))
			for point in tempDest:
				self.gameUnits[uID].AIBehaviors.addToPath(Vec3(4*point[0], 4*point[1], getHeight(point, mainClass)-3))
			self.gameUnits[uID].AIBehaviors.startFollow()
			
		else:
			return None
				
	#	else:
	
	
	def tskMove(self, unitNumber):
		if (self.gameUnits[unitNumber].AIBehaviors.behaviorStatus('pathfollow') == 'done') or (self.gameUnits[unitNumber].AIBehaviors.behaviorStatus('pathfollow') == 'paused'):
			self.gameUnits[unitNumber].job = False
			return Task.done
			
		else:
			return Task.cont
			
		
	def tskWorld(self, task): # A task to update the units in the world
		self.AIWorld.update()
		base.cTrav2.traverse(render)

		for i in self.gameUnits:
	#		print self.gameUnits[i].uID
			if (self.gameUnits[i].AIBehaviors.behaviorStatus('pathfollow') == 'done'):
				self.gameUnits[i].AIBehaviors.pauseAi("pathfollow")
			elif (self.gameUnits[i].AIBehaviors.behaviorStatus('pathfollow') == 'active'):
				self.gameUnits[i].modelNode.setP(0)
		
		return Task.cont
		
	def getNearestAvailable(self, job):
		#searchX = 1000
		#searchY = 1000
		
		search = 1000
		
		if (len(job.position) == 2):
			position = (job.position[0]*4, job.position[1]*4)
			
		else:
			position = job.position
			
		for uID in self.gameUnits:
			unit = self.gameUnits[uID]
			print uID, unit.job
			if (unit.job == False) and (unit.dig != None):
				tempPos = abs(job.position[0] - unit.modelNode.getX()) + abs(job.position[1]-unit.modelNode.getY())
				if (tempPos < search):
					search = tempPos
					number = unit.uID
				#if ((unit.modelNode.getX() + unit.modelNode.getY())/2 < (searchX +searchY)/2):
				#	searchX = unit.modelNode.getX()
				#	searchY = unit.modelNode.getY()
				#	number = unit.uID
					
					return number
		#	else:
		#		return None
				
	def doJob(self, job, unitNumber, mainClass):
		def getNearTile(tileX,tileY):
			print mainClass.mapLoaderClass.tileArray[tileY+1][tileX].solid, mainClass.mapLoaderClass.tileArray[tileY-1][tileX].solid, mainClass.mapLoaderClass.tileArray[tileY][tileX-1].solid, mainClass.mapLoaderClass.tileArray[tileY][tileX+1].solid
			if (mainClass.mapLoaderClass.tileArray[tileY+1][tileX].solid == False):
				return (tileX,tileY+1)
				
			elif (mainClass.mapLoaderClass.tileArray[tileY-1][tileX].solid == False):
				return (tileX,tileY-1)
			
			elif (mainClass.mapLoaderClass.tileArray[tileY][tileX+1].solid == False):
				return (tileX+1,tileY)
			
			elif (mainClass.mapLoaderClass.tileArray[tileY][tileX-1].solid == False):
				return (tileX-1,tileY)
			
			else:
				print 'NOOOO'
				
		def toTile(numberToRound):
			numberToRound = round(numberToRound)
			if (numberToRound % 4 == 1):
				numberToRound -= 1
			elif (numberToRound % 4 == 2):
				numberToRound -= 2
			elif (numberToRound % 4 == 3):
				numberToRound += 1
			else:
				pass
			return int(numberToRound)
			
		if (job.type == "drill"):
			tempTile = getNearTile(job.position[0],job.position[1])#(toTile(job.position[0]),toTile(job.position[1]))
			print '##'+str(tempTile)
			if (tempTile != None):
			#	mainClass.priorities.taskDict.remove(job)
				self.moveTo(mainClass, (tempTile[0]*4, tempTile[1]*4), unitNumber)
				self.gameUnits[unitNumber].job = ["drill",(job.position[0],job.position[1])]
			
			taskMgr.add(self.mineWall, "Unit finishing", extraArgs = [job, mainClass, unitNumber])
				
	def mineWall(self, job, mainClass, unitNumber):
	#	print self.gameUnits[unitNumber].job
		if (self.gameUnits[unitNumber].job[0] == "drill"):
		#	print self.gameUnits[unitNumber].AIBehaviors.behaviorStatus('pathfollow')
			if (self.gameUnits[unitNumber].AIBehaviors.behaviorStatus('pathfollow') == 'done') or (self.gameUnits[unitNumber].AIBehaviors.behaviorStatus('pathfollow') == 'paused'):
			#	if (self.gameUnits[unitNumber].job != False):
				mainClass.mineWall(mainClass.mapLoaderClass.tileArray[self.gameUnits[unitNumber].job[1][1]][self.gameUnits[unitNumber].job[1][0]])
				self.gameUnits[unitNumber].job = False
			#	else:
			#		print 'eh?'
				return Task.done
				
			else:
				return Task.cont
				
		elif (self.gameUnits[unitNumber].job == "selected"):
			return Task.cont
				
		else:
			mainClass.priorities.taskDict["drill"].append(job)
			return Task.done
			
			
class Unit:
	def __init__(self, unitID, position, mainClass):
	#	self = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]])
		
		self.model = mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].model
		
		self.fullName = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].fullName)
		self.HP = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].HP)
		self.info = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].info)
		self.moveType = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].moveType)
		self.model = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].model)
		self.radius = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].radius)
		self.mass = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].mass)
		self.startForce = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].startForce)
		self.maxForce = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].maxForce)
		self.dig = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].dig)
		self.reinforce = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].reinforce)
		self.shovel = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].shovel)
		self.hold = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].hold)
		self.modelHeight = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].modelHeight)
		self.selectScale = copy.copy(mainClass.unitHandler.unitDict[mainClass.unitHandler.main['units'][unitID]].selectScale)
		self.job = False
		
		self.uID = mainClass.unitHandler.unitUniqueID
		print self.uID
		self.modelNode = loader.loadModel(self.model)
		self.modelNode.setName('unit ' + str(self.uID).zfill(3))
		self.modelNode.reparentTo(render)
		self.modelNode.setPos(position)
		self.modelNode.setCollideMask(BitMask32.bit(1))
		
		self.select = OnscreenImage(image = 'data/models/game/selected.png')
		self.select.setScale(float(self.selectScale))
		self.select.reparentTo(self.modelNode)
		self.select.setZ(float(self.modelHeight)/2)
		self.select.setTransparency(TransparencyAttrib.MAlpha)
		self.select.setBillboardPointEye()
		self.select.hide()
		
		self.groundRay = CollisionRay()
		self.groundRay.setOrigin(0,0,100)
		self.groundRay.setDirection(0,0,-1)
		
		self.groundCol = CollisionNode('unit Ray')
		self.groundCol.addSolid(self.groundRay)
		self.groundCol.setTag('units','ray1')
		
		self.groundCol.setFromCollideMask(BitMask32.bit(0))
		self.groundCol.setIntoCollideMask(BitMask32.allOff())
		self.groundColNp = self.modelNode.attachNewNode(self.groundCol)
		self.groundColNp.setPos(0,0,0)
		self.groundHandler = CollisionHandlerFloor()
		self.groundHandler.setMaxVelocity(100)
		
		base.cTrav2.addCollider(self.groundColNp, self.groundHandler)

		self.groundHandler.addCollider(self.groundColNp, self.modelNode)
		
		self.AI = AICharacter(self.fullName,
								self.modelNode,
								self.mass*2,
								self.startForce*2,
								self.maxForce*2)
		mainClass.unitHandler.AIWorld.addAiChar(self.AI)
		self.AIBehaviors = self.AI.getAiBehaviors()
		
		if (self.moveType == 'ground'):
			self.aStar = astar.aStar(mainClass.unitHandler.meshes.landMesh, mainClass)
		elif (self.moveType == 'water'):
			self.aStar = astar.aStar(mainClass.unitHandler.meshes.waterMesh, mainClass)
		elif (self.moveType == 'air'):
			self.aStar = astar.aStar(mainClass.unitHandler.meshes.airMesh, mainClass)
		
		print self
		
	#	mainClass.unitHandler.unitUniqueID += 1