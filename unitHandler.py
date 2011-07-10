from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.task.Task import *
from direct.showbase.DirectObject import DirectObject
from panda3d.ai import *

import random, sys, os, math, copy

class world:
	def __init__(self, unitDict, tileList):
		self.AIWorld = AIWorld(render)
		self.cTrav = CollisionTraverser('world') # TBC
		self.cTrav.showCollisions(render)
		
		base.cTrav = self.cTrav
		
#		self.cTrav.traverse(render)
		
		self.unitDict = unitDict # The dictionary created of all the units and their keys by the parser
		
		self.gameUnits = {} # A dictionary containing all the units in the game, with each unit's ID as its key
		self.unitMoving = {} # Shows whether a unit is moving or not
		
		self.unitUniqueID = 0
	
		taskMgr.add(self.updateWorld, "World task")
		
	def loadWalls(self, unitNumber, tileList):
		unit = self.gameUnits[unitNumber]
		for row in tileList:
			for tile in row:
				print tile.name, tile.solid
				if (tile.solid == True):
					print tile.model
					unit.AIbehaviors.addStaticObstacle(tile.model)

	def reloadWallsAll(self, tileList):
		for unitKey in self.gameUnits:
			if (self.unitMoving[unitKey] == 0):
				self.gameUnits[unitKey].AIbehaviors.removeAi("all")
				#self.gameUnits[unitKey].AIbehaviors.initPathFind("data/models/game/navmesh2.csv")
				for row in tileList:
					for tile in row:
						if (tile.solid == True):
							print tile.model
#							self.gameUnits[unitKey].AIbehaviors.addStaticObstacle(tile.model)
	
##		pass
	
	def updateWorld(self, task):
		self.AIWorld.update()
#		print self.gameUnits[0].AIbehaviors.behaviorStatus("pathfollow"), self.gameUnits[0].actor.getPos()
		
		for unit in self.gameUnits:
			if (self.gameUnits[unit].AIbehaviors.behaviorStatus("pathfollow") != "active"):
				self.unitMoving[unit] = 0

#			else:
#				self.unitMoving[unit] = 0
				
			if (self.unitMoving[unit] != 0):
				self.unitTask(unit)
		
		return Task.cont
		
	def unitTask(self, unitUniqueID):
        # Now check for collisions.

		self.cTrav.traverse(render)

        # Adjust ralph's Z coordinate.  If ralph's ray hit terrain,
        # update his Z. If it hit anything else, or didn't hit anything, put
        # him back where he was last frame.

        #print(self.ralphGroundHandler.getNumEntries())

		entries = []
		
		for i in range(self.gameUnits[unitUniqueID].actor.groundHandler.getNumEntries()):
			entry = self.gameUnits[unitUniqueID].actor.groundHandler.getEntry(i)
			entries.append(entry)
		entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
									x.getSurfacePoint(render).getZ()))
		if (len(entries)>0) and (entries[0].getIntoNode().getName() == "Tile"):
			self.gameUnits[unitUniqueID].actor.setZ(entries[0].getSurfacePoint(render).getZ())
#		else:
#			self.gameUnits[unitUniqueID].AIbehaviors.pauseAi("pathfollow")
##			print len(entries), entries[0].getIntoNode().getName()
#			print 'hi'

		self.gameUnits[unitUniqueID].actor.setP(0)
		
	def moveUnit(self, unitUniqueID, target):
		print unitUniqueID, target
		def roundCoords(coord):
			coord2 = list(coord)
			for i in range(2):
				coord2[i] = float(int(coord2[i]))
			coord = tuple(coord2)
			return coord
				
		self.gameUnits[unitUniqueID].AIbehaviors.pauseAi("pathfollow")
		try:
			self.gameUnits[unitUniqueID].AIbehaviors.pathFindTo(target, "addPath")
		except:
			self.gameUnits[unitUniqueID].actor.setPos(roundCoords(self.gameUnits[unitUniqueID].actor.getPos()))
			self.gameUnits[unitUniqueID].AIbehaviors.pathFindTo(target, "addPath")
			
		self.unitMoving[unitUniqueID] = target
		
class unit:
	def addNewModel(self, unitNumber, position, world, tileList):
		unit = copy.copy(world.unitDict[unitNumber]) # gets the data from the dictionary of the units
		
		unit.ID = world.unitUniqueID
		world.unitUniqueID += 1
		
		unit.actor = Actor(unit.model)
		unit.actor.reparentTo(render)
		unit.actor.setPos(position)
		
		unit.actor.setCollideMask(0x2)
		
		#unit.cTrav = CollisionTraverser()
		
		unit.actor.groundRay = CollisionRay() # Makes a collisionNode for the unit, to set it to the right height.
		unit.actor.groundRay.setOrigin(0,0,1000)
		unit.actor.groundRay.setDirection(0,0,-1)
		unit.actor.groundCol = CollisionNode('UnitRay')
		unit.actor.groundCol.addSolid(unit.actor.groundRay)
		unit.actor.groundCol.setFromCollideMask(BitMask32.bit(0))
		unit.actor.groundCol.setIntoCollideMask(BitMask32.allOff())
		unit.actor.groundColNP = unit.actor.attachNewNode(unit.actor.groundCol)
		unit.actor.groundHandler = CollisionHandlerQueue()
		
		world.cTrav.addCollider(unit.actor.groundColNP, unit.actor.groundHandler)
		
		unit.actor.groundColNP.show()
#		world.cTrav.showCollisions(render)
		
		unit.AIChar = AICharacter(unit.name,
									unit.actor, 
									2*unit.mass,
									2*unit.startforce,
									2*unit.maxforce)
#		self.world = world
		world.AIWorld.addAiChar(unit.AIChar)
		unit.AIbehaviors = unit.AIChar.getAiBehaviors()
		unit.AIbehaviors.initPathFind("data/models/game/navmesh2.csv")
		
		world.gameUnits[unit.ID] = unit
		world.unitMoving[unit.ID] = 0
		world.loadWalls(unit.ID, tileList)
		
		print world.gameUnits