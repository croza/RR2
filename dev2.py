import direct.directbase.DirectStart
import os, sys, math, random
from direct.interval.IntervalGlobal import *
from direct.fsm import FSM
from direct.fsm import State
from panda3d.core import *
from random import randint, random

from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.task import *
from direct.actor.Actor import Actor
from panda3d.ai import *
from direct.gui.OnscreenText import OnscreenText

class world(DirectObject):
	def __init__(self):
		self.values()
		self.loadSurf()
		self.loadWorld()
		self.loadLight()
		
	def values(self):
		self.mapDir = "./ten/"
		self.SurfDir = open(self.mapDir+"Surf.map")
		
		self.Surf = self.SurfDir.read()
		self.SurfList = list(self.Surf)
		
		self.SurfSizeData = self.SurfList[4]
		self.SurfXData = self.SurfList[8]
		self.SurfYData = self.SurfList[12]
		self.SurfSize = int(os.path.getsize(self.mapDir+"Surf.map"))
		
		self.SurfSizeHex = self.SurfSizeData.encode("hex")
		self.SurfXHex = self.SurfXData.encode("hex")
		self.SurfYHex = self.SurfYData.encode("hex")
		
		#self.SurfSize = int(str(self.SurfSizeHex), 16)
		self.SurfX = int(str(self.SurfXHex), 16)
		self.SurfY = int(str(self.SurfYHex), 16)
		
		self.actualSurfSize = self.SurfX*self.SurfY
		
	def loadSurf(self):
		self.SurfStart = 16
		self.SurfNumber = 1
		
		self.SurfData = []
		
		while(self.SurfStart < self.SurfSize-(2*self.SurfX)):
			self.SurfData.append(str(self.SurfList[self.SurfStart]).encode("hex"))
			self.SurfStart += 2
			self.SurfNumber += 1
		print 'Surf loaded.'
		#print self.SurfData.keys()
		
	def loadWorld(self):
		self.loadWorldNumber = 1 # All models including ones that aren't rendered ect.
		self.loadWorldNumber2 = 1 # Just the rendered models.
		
		self.loadWorldNumber3 = 1 # Storage only, really
		self.lineNumber = 0 # Line numbers
		
		self.rowNumber = []
		self.rowData = []
		
		self.square = []
		self.squareData = []
		
		self.worldSplit = 0
		
		while(self.loadWorldNumber3 < self.SurfNumber): # Puts the list created by loadSurf into 'lines'
			self.nextSplit = self.worldSplit + self.SurfX # Sets where to finish the 'split'
			
			self.loadWorldTemp1 = 0
			self.rowData = []
			
			while(self.worldSplit  < self.nextSplit):
				self.rowData.append(self.SurfData[self.worldSplit])
				self.worldSplit += 1
				
			self.rowNumber.append(self.rowData)			
			print str(self.rowData)
			
			self.loadWorldNumber3 += self.SurfX
			self.lineNumber += 1
			
		print self.rowNumber
		print self.lineNumber
		
		
		#self.startCoordX = -4*self.SurfX # Setting the start position ~~NOT NEEDED
		
		self.square = {}
		
		self.coordX = -2 # Starting coords
		self.coordY = -2
		self.coordZ = 0
		
		self.squareRowNumber = 0 # The current number of the square
		self.currentRow = 0 # The current row of the square ~~NOTE that row 0 is at the top, and it goes DOWNWARDS
		
		self.row = []
		self.world = []
		
		print self.SurfX
		
		self.tempSquareData = [] # Temporary value
		
		while(self.currentRow < self.SurfY-1): # While the square is within the grid (??)
			#print self.squareRowNumber,self.currentRow,self.loadWorldNumber2
			
			if(self.squareRowNumber < self.SurfX-1): #As long as the square is in the row (not the extra one on the end)
				#print self.currentRow
				self.currentRowData = self.rowNumber[self.currentRow]
				self.currentSquareData = self.currentRowData[self.squareRowNumber]
				
				#print self.currentSquareData
				
				self.tempsquareData = []
				self.row = []
				self.tempSquareData = ''
				
				if(str(self.currentSquareData) == '01'):
					self.row.append(rock01())
					self.type = rock01()
					
				elif(str(self.currentSquareData) == '02'):
					self.row.append(rock02())
					self.tempSquareData = 'rock02'
					self.type = rock02()
					
				elif(str(self.currentSquareData) == '03'):
					self.row.append(rock03())
					self.tempSquareData = 'rock03'
					self.type = rock03()
					
				elif(str(self.currentSquareData) == '04'):
					self.row.append(rock04())
					self.tempSquareData = 'rock04'
					self.type = rock04()
					
				elif(str(self.currentSquareData) == '05'):
					self.row.append(rock05())
					self.tempSquareData = 'rock05'
					self.type = rock05()
					
				elif(str(self.currentSquareData) == '06'):
					self.row.append(rock06())
					self.tempSquareData = 'rock06'
					self.type = rock06()
					
				elif(str(self.currentSquareData) == '08'):
					self.row.append(rock08())
					self.tempSquareData = 'rock08'
					self.type = rock08()
					
				elif(str(self.currentSquareData) == '09'):
					self.row.append(rock09())
					self.tempSquareData = 'rock09'
					self.type = rock09()
					
				elif(str(self.currentSquareData) == '0a'):
					self.row.append(rock0a())
					self.tempSquareData = 'rock0a'
					self.type = rock0a()
					
				elif(str(self.currentSquareData) == '0b'):
					self.row.append(rock0b())
					self.tempSquareData = 'rock0b'
					self.type = rock0b()
				
				#self.world.append(self.row)
				
				#self.squareLoader = (self.row[self.squareRowNumber])
				#print self.squareLoader
				#print self.type
				self.squareLoader2 = loader.loadModel(str(self.type.model))
				
				self.square[self.loadWorldNumber2] = self.squareLoader2
				self.square[self.loadWorldNumber2].setPos(self.coordX,self.coordY,0)
				self.square[self.loadWorldNumber2].reparentTo(render)
				
				#print self.square[self.loadWorldNumber2]
				
				self.loadWorldNumber += 1
				self.loadWorldNumber2 += 1
				self.coordX += 4
				self.squareRowNumber += 1
				
			else:
				#print 'poo'
				self.world.append(self.row)
				self.row = []
				self.squareRowNumber = 0
				#print self.world
				self.currentRow += 1
				self.coordY -= 4
				self.coordX = -2
				
		#print self.world
		
	def loadLight(self): #Sets the lights
		plight = AmbientLight('my plight')
		plight.setColor(VBase4(1.0,1.0,1.0,1))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)
		
class rock01:
	def __init__(self):
		self.type = 'Solid Rock'
		self.model = './models/World/solidrock'
		self.solid = True
		
class rock02:
	def __init__(self):
		self.type = 'Hard Rock'
		self.model = './models/World/hardrock'
		self.solid = True
		
class rock03:
	def __init__(self):
		self.type = 'Loose Rock'
		self.model = './models/World/looserock'
		self.solid = True
		
class rock04:
	def __init__(self):
		self.type = 'Dirt'
		self.model = './models/World/dirt'
		self.solid = True
		
class rock05:
	def __init__(self):
		self.type = 'Ground'
		self.model = './models/World/ground'
		self.solid = False
		
class rock06:
	def __init__(self):
		self.type = 'Lava'
		self.model = './models/World/lava'
		self.solid = False
		
class rock08:
	def __init__(self):
		self.type = 'Ore Seam'
		self.model = './models/World/oreseam'
		self.solid = True
		
class rock09:
	def __init__(self):
		self.type = 'Water'
		self.model = './models/World/water'
		self.solid = False
		
class rock0a:
	def __init__(self):
		self.type = 'Energy Crystal Seam'
		self.model = './models/World/energycrystalseam'
		self.solid = True
		
class rock0b:
	def __init__(self):
		self.type = 'Recharge Seam'
		self.model = './models/World/rechargeseam'
		self.solid = True
		
