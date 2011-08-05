# With a lot of help from scripts by pandai

import direct.directbase.DirectStart
from pandac.PandaModules import CollisionTraverser, CollisionNode
from pandac.PandaModules import CollisionHandlerQueue, CollisionRay
from pandac.PandaModules import Filename
from pandac.PandaModules import PandaNode, NodePath, Camera, TextNode
from pandac.PandaModules import Vec3, Vec4, BitMask32
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math

from direct.interval.IntervalGlobal import *

class thirdPerson(DirectObject):
	def __init__(self, parserClass, mainClass, mapLoaderClass, modelLoaderClass):
		self.switchState = False
		
		self.keyMap = {"left":0, "right":0, "forward":0, "backward":0}
		self.ralph = Actor("data/models/units/ralph/ralph",
								{"run":"data/models/units/ralph/ralph-run",
								"walk":"data/models/units/ralph/ralph-walk"})
		self.ralph.reparentTo(render)
		self.ralph.setPos(42, 30, 0)
		self.ralph.setScale(0.1)
		
		self.accept("escape", sys.exit)
		self.accept("arrow_left", self.setKey, ["left",1])
		self.accept("arrow_left-up", self.setKey, ["left",0])
		self.accept("arrow_right", self.setKey, ["right",1])
		self.accept("arrow_right-up", self.setKey, ["right",0])
		self.accept("arrow_up", self.setKey, ["forward",1])
		self.accept("arrow_up-up", self.setKey, ["forward",0])
		self.accept("arrow_down", self.setKey, ["backward",1])
		self.accept("arrow_down-up", self.setKey, ["backward",0])
		
		self.isMoving = False
		
		self.cTrav = CollisionTraverser()

		self.ralphGroundRay = CollisionRay()
		self.ralphGroundRay.setOrigin(0,0,1000)
		self.ralphGroundRay.setDirection(0,0,-1)
		self.ralphGroundCol = CollisionNode('ralphRay')
		self.ralphGroundCol.addSolid(self.ralphGroundRay)
		self.ralphGroundCol.setFromCollideMask(BitMask32.bit(0))
		self.ralphGroundCol.setIntoCollideMask(BitMask32.allOff())
		self.ralphGroundColNp = self.ralph.attachNewNode(self.ralphGroundCol)
		self.ralphGroundHandler = CollisionHandlerQueue()
		self.cTrav.addCollider(self.ralphGroundColNp, self.ralphGroundHandler)
		#self.ralphGroundCol.show()
		
		base.cam.reparentTo(self.ralph)
		base.cam.setPos(0, 9, 7)
		self.floater2 = NodePath(PandaNode("floater2"))
		self.floater2.reparentTo(self.ralph)
		self.floater2.setZ(self.floater2.getZ() + 6)
		base.cam.lookAt(self.floater2)

		# Uncomment this line to see the collision rays
		self.ralphGroundColNp.show()
#		self.camGroundColNp.show()
	   
		#Uncomment this line to show a visual representation of the 
		#collisions occuring
		self.cTrav.showCollisions(render)
		
		self.floater = NodePath(PandaNode("floater"))
		self.floater.reparentTo(render)
		
		taskMgr.add(self.move, "movingTask", extraArgs = [mainClass, parserClass, mapLoaderClass, modelLoaderClass])
		
	#Records the state of the arrow keys
	def setKey(self, key, value):
		self.keyMap[key] = value
		
	def move(self, mainClass, parserClass, mapLoaderClass, modelLoaderClass):
		# Get the time elapsed since last frame. We need this
		# for framerate-independent movement.
		elapsed = globalClock.getDt()
		
		# save ralph's initial position so that we can restore it,
		# in case he falls off the map or runs into something.

		startpos = self.ralph.getPos()
		
		# If a move-key is pressed, move ralph in the specified direction.

		if (self.keyMap["left"] != 0):
			self.ralph.setH(self.ralph.getH() + elapsed*300)
		if (self.keyMap["right"] != 0):
			self.ralph.setH(self.ralph.getH() - elapsed*300)
		if (self.keyMap["forward"] != 0):
			self.ralph.setY(self.ralph, -(elapsed*25))
		if (self.keyMap["backward"] != 0):
			self.ralph.setY(self.ralph, +(elapsed*10))
			
		if (self.keyMap["forward"] != 0) or (self.keyMap["left"] != 0) or (self.keyMap["right"] != 0):
			if self.isMoving is False:
				self.ralph.loop("run")
				self.isMoving = True
				
		elif (self.keyMap["backward"] != 0):
			if self.isMoving is False:
				self.ralph.stop()
				self.ralph.pose("walk",5)
				self.isMoving = False
				
		else:
			if self.isMoving:
				self.ralph.stop()
				self.ralph.pose("walk",5)
				self.isMoving = False
				
		# Now check for collisions.

		self.cTrav.traverse(render)

		# Adjust ralph's Z coordinate.  If ralph's ray hit terrain,
		# update his Z. If it hit anything else, or didn't hit anything, put
		# him back where he was last frame.

		entries = []
		for i in range(self.ralphGroundHandler.getNumEntries()):
			entry = self.ralphGroundHandler.getEntry(i)
			entries.append(entry)
		entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
									 x.getSurfacePoint(render).getZ()))	
		
#		if (len(entries)>0):
#			print entries[0].getIntoNode().getName()[0:4]
		
		if (len(entries)>0) and (entries[0].getIntoNode().getName()[0:4] == "tile"):
			self.something = False
			self.isMining = False
			self.ralph.setZ(entries[0].getSurfacePoint(render).getZ())
			
		elif (len(entries)>0) and (entries[0].getIntoNode().getName()[0:5] == "solid"):
			self.ralph.setPos(startpos)
			x = int(entries[0].getIntoNode().getName()[len(entries[0].getIntoNode().getName())-6:len(entries[0].getIntoNode().getName())-4])
			y = int(entries[0].getIntoNode().getName()[len(entries[0].getIntoNode().getName())-2:])
			if (mapLoaderClass.tileArray[y][x].drillTime != None):
				mainClass.changeTile(mapLoaderClass.tileArray[y][x], 0, parserClass, modelLoaderClass, mapLoaderClass)
		else:
			self.ralph.setPos(startpos)
		
		self.ralph.setP(0)
		return Task.cont