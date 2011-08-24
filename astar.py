import math
import copy

from pandac.PandaModules import *

class grid:
	def __init__(self, mainClass):
#		self.allMesh = []
		
		self.landMesh = []
		self.waterMesh = []
		self.airMesh = []
		
		for row in mainClass.mapLoaderClass.tileArray:
			landRow = []
			waterRow = []
			airRow = []
			
			for tile in row:
				if tile.walkable == True:
					landRow.append(True)
				else:
					landRow.append(False)
					
				if tile.water == True:
					waterRow.append(True)
				else:
					waterRow.append(False)
					
				if (tile.lava == True) or (tile.water == True) or (tile.walkable == True):
					airRow.append(True)
				else:
					airRow.append(False)
				
			self.landMesh.append(landRow)
			self.waterMesh.append(waterRow)
			self.airMesh.append(airRow)
		
class Node:
	def __init__(self, x, y, G, H, parent): # parent being the position of the node's parent
		self.x = x
		self.y = y
		self.g = G
		self.h = H
		self.f = G + H
		self.parent = parent
		
class aStar:
	def __init__(self, mesh, mainClass):
		self.mesh = mesh
		
		self.width = mainClass.mapX - 1
		self.height = mainClass.mapY - 1
		
	def moveTo(self, startNode, endPos):
		def calcH(position, finish): # A function to calculate the H value
			dx = position[0] - finish[0]
			dy = position[1] - finish[1]
			return math.sqrt( dx * dx + dy * dy ) * 6
			
		def calcG(currentNode, nodeMovingToPos):
			if ((nodeMovingToPos[0] == currentNode.x + 1) or (nodeMovingToPos[0] == currentNode.x - 1)) and ((nodeMovingToPos[1] == currentNode.y + 1) or (nodeMovingToPos[1] == currentNode.y - 1)):
				self.G += 8
				return self.G
			else:
				self.G += 6
				return self.G
				
		def recalcG(nodeMovingTo, currentNode):
			if ((nodeMovingTo.x == currentNode.x + 1) or (nodeMovingTo.x == currentNode.x - 1)) and ((nodeMovingTo.y == currentNode.y + 1) or (nodeMovingTo.y == currentNode.y - 1)):
				return nodeMovingTo.g + 8
			else:
				return nodeMovingTo.g + 6
			
		def getSurround(node):
			surround = []
#			surround.append((node.x-1, node.y-1)) # BL
			surround.append((node.x-1, node.y)) # BC
#			surround.append((node.x-1, node.y+1)) # BR
			surround.append((node.x, node.y-1)) # CL

			surround.append((node.x, node.y+1)) # CR
#			surround.append((node.x+1, node.y-1)) # TL
			surround.append((node.x+1, node.y)) # TC
#			surround.append((node.x+1, node.y+1)) # TR
			return surround
			
		openList = []
		closedList = []
				
		endPosNode = self.roundToTile(endPos)
		startPosNode = self.roundToTile((startNode.getPos()))
		
		ID = 0
		
		self.G = 0
		
		openList.append(Node(startPosNode[0], startPosNode[1], self.G, calcH(startPosNode, endPosNode), None))
		
		finished = False
		
		while finished != True:
			sorted(openList, key = lambda tile: tile.f)
			if (len(openList) >= 1):
				currentNode = copy.copy(openList[0])
				openList.remove(openList[0])
				closedList.append(currentNode)
				if ((currentNode.x, currentNode.y) == endPosNode): # If it is the end node
					print 'yay'
					
					endList = [(currentNode.x, currentNode.y, 0)]
					endNode = False
					
					while endNode != True:
						currentNode = currentNode.parent
						endList.append((currentNode.x, currentNode.y, 0))
						
						if currentNode.parent == None:
							endNode = True
							print endList
							return endList
						
					finished = True
				else: # If not the end node
					surround = getSurround(currentNode)
					surroundNo = 0
					for node in surround: # For each of the potential surrounding nodes					
						if (0<= node[0] <= self.width) and (0<= node[1] <= self.height):
							if (self.mesh[node[1]][node[0]] == True):	
								oList = False
								cList = False
								
								for n in openList: # If it is in the openList, change oList to the node in the list (bad explanation)
									if (n.x == node[0]) and (n.y == node[1]):
										oList = n
								for m in closedList:
									if (m.x == node[0]) and (m.y == node[1]):
										cList = m
										
								if (cList == False): # If not in the closedList
									if (oList == False): # If not in the openlist, put it in the openList
												openList.append(Node(node[0], node[1], calcG(currentNode, node), calcH(node, endPosNode), currentNode))
									else: # Already on the openList, so if the current node is a more cost efficient parent, adjust the parenting
										if (recalcG(currentNode, oList) < oList.g):
											oList.parent = currentNode
											oList.g = recalcG(currentNode, oList)

							surroundNo += 1
			else:
				print 'No path available'
				finished = True
				return []	
				
	def roundToTile(self, coordsToRound):
		def toTile(numberToRound):
			if (numberToRound % 4 == 1):
				numberToRound -= 1
			elif (numberToRound % 4 == 2):
				numberToRound -= 2
			elif (numberToRound % 4 == 3):
				numberToRound += 1
			else:
				pass
			return numberToRound
				
		currX = round(coordsToRound[0])
		currY = round(coordsToRound[1])
		
		currX = toTile(currX)/4
		currY = toTile(currY)/4

		return (int(currX), int(currY))