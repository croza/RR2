# Lots of thanks to the guys at Pandai for their examples and work, most of this has been copied and pasted from one of their examples, so credit to them.
# It's here to show that pathfinding can work, NOT to be kept permanently
# NEEDS TO BE RE-WRITTEN

from pandac.PandaModules import * # Not sure exactly how many of these are needed, and they need to be simplified.
from direct.showbase.DirectObject import DirectObject
from direct.task import *
from direct.interval.IntervalGlobal import *
from direct.fsm import FSM
from direct.fsm import State
from direct.actor.Actor import Actor
from panda3d.ai import *
import math
import random, sys, os, math
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText

speed = 1

class basicMoving(DirectObject):
	def __init__(self):
		self.keyMap = {"left":0, "right":0, "up":0, "down":0}
		
		modelStartPos = (6, 6, 2) # The starting coords of the model)
		#self.Model = Actor("data/models/units/lowpol-legohead") # The model directory
		self.Model = loader.loadModel("data/models/units/lowpol-legohead")
		self.Model.reparentTo(render)
		self.Model.setPos(modelStartPos)
		
		self.pointer = loader.loadModel("data/models/game/arrow") # Directory of the pointer (we will need to make a new model for this, and it will have to be rendered on -and at- mouse click)
		self.pointer.setColor(1,0,0)
		self.pointer.setPos(0,0,0)
		self.pointer.setScale(2)
		self.pointer.reparentTo(render)
		
		self.pointer_move = False
		
		self.setAI()
		
	def setAI(self):
		self.AIworld = AIWorld(render) # This was commented as 'Creating AI World'?
		
		self.accept("enter", self.setMove) # Key accepting
		
		self.accept("arrow_left", self.setKey, ["left",1])
		self.accept("arrow_right", self.setKey, ["right",1])
		self.accept("arrow_up", self.setKey, ["up",1])
		self.accept("arrow_down", self.setKey, ["down",1])
		self.accept("arrow_left-up", self.setKey, ["left",0])
		self.accept("arrow_right-up", self.setKey, ["right",0])
		self.accept("arrow_up-up", self.setKey, ["up",0])
		self.accept("arrow_down-up", self.setKey, ["down",0])
		
		self.AIchar = AICharacter("model",self.Model, 200, 0.05, 15)
		self.AIworld.addAiChar(self.AIchar)
		self.AIbehaviors = self.AIchar.getAiBehaviors()
		
		self.AIbehaviors.initPathFind("data/models/game/navmesh2.csv") # A better one of these may needed to be generated (a navmesh tells the AI which points it can navigate to)
     
		taskMgr.add(self.AIUpdate,"AIUpdate") # Updates the target of the model
	
		#movement task
		taskMgr.add(self.Mover,"Mover") # The moving pointer stuff
		
	def setMove(self):
		self.AIbehaviors.pathFindTo(self.pointer)
		
	def AIUpdate(self,task): # The name says it all
		self.AIworld.update()

		return Task.cont

	def setKey(self, key, value): # Decides what to do with your pressed key
		self.keyMap[key] = value
        
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
            
		if(self.pointer_move == True and self.box != 0): # Press enter to start
			self.box.setPos(self.pointer.getPos())
                
		return Task.cont