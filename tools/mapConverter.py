# TBC add .cfg for the map converter
#
# Only to be used with maps made with Cyrem's map creator

import os
import sys

directory = raw_input("Please enter the directory (folder) of the map wished to be converted (e.g. 'map/'): ")
X = int(raw_input("Please enter the width of the map (note that it is one more than what you put into the creator's size to be): "))
Y = int(raw_input("Please enter the height of the map (same as with the width, one more than what you think it is: "))

mapFiles = ['Surf.map', 'Cror.map', 'Dugg.map', 'Emrg.map', 'Erod.map', 'Fall.map', 'High.map', 'Path.map', 'Surf.map', 'Tuto.map']
otherFiles = ['ObjectList.ol']

def ifExist(file2):
	if (os.path.exists(directory+file2) == True):
		pass
	else:
		raise "One or more of the .map files doesn't exist."
		
		
def clipFile(file2):
	tempFile = open(directory+file2)
	tempData = tempFile.read()

	if (len(tempData) != 2*(X*Y)+16):
		raise "This file has a bad length."
	
	tempData = tempData[16:]
	tempData = tempData[:len(tempData)-(2*X)]
	#print tempData.encode("hex")
	
	endList = [] # tempFile will be read, and the bits needed will be stored here
	endFile = ''
	
	tempX = 1
	charNumber = 1
	
	for i in range(len(tempData)): # Cuts the file up into relevant sections (a list of numbers)
		if (i % 2 == 0):
			if (i % X == 0):
				pass
			else:
				endList.append(int('0x'+tempData[i].encode("hex"), 0))
	
	for value in endList:
		endFile = endFile+str(value)
		
	#print endFile
	
	return endFile
	
def makeFile(fileData, name):
	directory2 = directory+'converted/'
	
	if (not os.path.exists(directory2)):
		os.makedirs(directory2)
		
	newFileDir = open(directory2+name, "w")
	newFileDir.write(newFile)
	
def makeConfig():
	configFile = open(directory+'/converted/map.cfg', "w")
	configStr = '[map]\nname: <insert name in the map.cfg file>\nbriefing: <insert breifing>\ndesc: <insert description>\nscript: <insert scripts>\nwidth: '+str(X-1)+'\nheight: '+str(Y-1)
	configFile.write(configStr)
		
for file in mapFiles:
	ifExist(file)
	print file
	newFile = clipFile(file)
	makeFile(newFile, file)
print 'map.cfg'
makeConfig()
