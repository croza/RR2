import direct.directbase.DirectStart
#from pandac.PandaModules import CollisionTraverser,CollisionNode
#from pandac.PandaModules import CollisionHandlerQueue,CollisionRay
#from pandac.PandaModules import Filename
#from pandac.PandaModules import PandaNode,NodePath,Camera,TextNode
#from pandac.PandaModules import Vec3,Vec4,BitMask32
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.task.Task import *
from direct.showbase.DirectObject import DirectObject

#from direct.interval.IntervalGlobal import *
#from direct.fsm import FSM
#from direct.fsm import State
from direct.gui.DirectGui import *

import random, sys, os, math

from panda3d.ai import *

speed = 1

class HeightMoving(DirectObject):
	def __init__(self):
		self.switchState = True
		self.switchCam = False
		self.path_no = 1
		self.keyMap = {"left":0, "right":0, "up":0, "down":0}
		base.win.setClearColor(Vec4(0,0,0,1))
		
		ActorStartPos = Vec3(6, 6, 10)
		self.Actor = Actor("data/models/units/lowpol-legohead")
		self.Actor.reparentTo(render)
		self.Actor.setScale(0.3)
		
		self.Actor.setPos(ActorStartPos)
		self.ActorAI = Actor("data/models/units/lowpol-legohead")
		 
		self.pointer = loader.loadModel("data/models/game/arrow") # Directory of the pointer (we will need to make a new model for this, and it will have to be rendered on -and at- mouse click)
		self.pointer.setColor(1,0,0)
		self.pointer.setPos(0,0,0)
		self.pointer.setScale(2)
		self.pointer.reparentTo(render)
		
		self.floater = NodePath(PandaNode("floater"))
		self.floater.reparentTo(render)
		
		self.accept("escape", sys.exit)
		
		self.isMoving = False
		
		self.cTrav = CollisionTraverser()

		self.ActorGroundRay = CollisionRay()
		self.ActorGroundRay.setOrigin(0,0,1000)
		self.ActorGroundRay.setDirection(0,0,-1)
		self.ActorGroundCol = CollisionNode('ActorRay')
		self.ActorGroundCol.addSolid(self.ActorGroundRay)
		self.ActorGroundCol.setFromCollideMask(BitMask32.bit(0))
		self.ActorGroundCol.setIntoCollideMask(BitMask32.allOff())
		self.ActorGroundColNp = self.Actor.attachNewNode(self.ActorGroundCol)
		self.ActorGroundHandler = CollisionHandlerQueue()
		self.cTrav.addCollider(self.ActorGroundColNp, self.ActorGroundHandler)
		
		self.ActorGroundColNp.show()
		# self.camGroundColNp.show()
		
		self.cTrav.showCollisions(render)
		
		self.setAI()
		
		self.pointer_move = False
		
		taskMgr.add(self.Mover,"Mover")

	def Mover(self,task): # Sets up the moving of the pointer etc.
		startPos = self.pointer.getPos()
		if (self.keyMap["left"]!=0):
			self.pointer.setPos(startPos + Point3(0.5*-speed,0,0))
		if (self.keyMap["right"]!=0):
			self.pointer.setPos(startPos + Point3(0.5*speed,0,0))
		if (self.keyMap["up"]!=0):
			self.pointer.setPos(startPos + Point3(0,0.5*speed,0))
		if (self.keyMap["down"]!=0):
			self.pointer.setPos(startPos + Point3(0,0.5*-speed,0))
                
		return Task.cont
		
	def setKey(self, key, value):
		self.keyMap[key] = value
		
	def move(self):
		elapsed = globalClock.getDt()
		startpos = self.Actor.getPos()
		
		self.cTrav.traverse(render)
		
		entries = []
		for i in range(self.ActorGroundHandler.getNumEntries()):
			entry = self.ActorGroundHandler.getEntry(i)
			entries.append(entry)
		entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
									x.getSurfacePoint(render).getZ()))
		if (len(entries)>0) and (entries[0].getIntoNode().getName() == "Tile"):
			self.Actor.setZ(entries[0].getSurfacePoint(render).getZ())
		else:
			self.Actor.setPos(startpos)
			
		self.Actor.setP(0)
		#return Task.cont
		
	def setAI(self):
		 #Creating AI World
		self.AIworld = AIWorld(render)
		
		self.accept("arrow_left", self.setKey, ["left",1])
		self.accept("arrow_right", self.setKey, ["right",1])
		self.accept("arrow_up", self.setKey, ["up",1])
		self.accept("arrow_down", self.setKey, ["down",1])
		self.accept("arrow_left-up", self.setKey, ["left",0])
		self.accept("arrow_right-up", self.setKey, ["right",0])
		self.accept("arrow_up-up", self.setKey, ["up",0])
		self.accept("arrow_down-up", self.setKey, ["down",0])
		self.accept("space", self.setMove)

		self.AIchar = AICharacter("actor",self.Actor, 60, 0.05, 25)
		self.AIworld.addAiChar(self.AIchar)
		self.AIbehaviors = self.AIchar.getAiBehaviors()
		self.AIbehaviors.initPathFind("data/models/game/navmesh2.csv")
        
		#AI World update        
		taskMgr.add(self.AIUpdate,"AIUpdate")
		
	def rounder(self, x, base = 2):
		return int(base * round(float(x)/base))
		
	def setMove(self):
        #self.AIbehaviors.addStaticObstacle(self.box)
        #self.AIbehaviors.addStaticObstacle(self.box1)
		self.mehPos = Vec3(self.rounder(self.pointer.getX()),self.rounder(self.pointer.getY()),int(self.pointer.getZ()))
		print self.mehPos
		self.AIbehaviors.pathFindTo(self.mehPos)
		#self.ralph.loop("run")
		
	def AIUpdate(self,task):
		self.AIworld.update()
		self.move()
		#print self.AIbehaviors.behaviorStatus("pathfollow")
		
		if(self.AIbehaviors.behaviorStatus("pathfollow") == "done"):
			self.TaskSomething = False
			return Task.done
		else:
			return Task.cont