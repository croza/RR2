# TBC add .cfg for the map converter
#
# Only to be used with maps made with Cyrem's map creator
#
# With thanks to DrakeMag from python-forum.org

import os
import sys

import struct

directory = raw_input("Please enter the directory (folder) of the map wished to be converted (e.g. 'map/'): ")
X = int(raw_input("Please enter the width of the map (note that it is one more than what you put into the creator's size to be): "))
Y = int(raw_input("Please enter the height of the map (same as with the width, one more than what you think it is: "))


#mapFiles = ['Cror.map', 'Dugg.map', 'Emrg.map', 'Erod.map', 'Fall.map', 'High.map', 'Path.map', 'Surf.map', 'Tuto.map']
mapFiles = ['Surf.map', 'High.map', 'Cror.map']
#otherFiles = ['ObjectList.ol']

def ifExist(file2):
	if (os.path.exists(directory+file2) == True):
		pass
	else:
		raise "One or more of the .map files doesn't exist."
		
		
def clipFile(file2):
	def to_binary(hex_string): # hex_string being hex(int); it will be dealt with here
		hex_string = hex_string[2:]
		if (len(hex_string) == 0):
			hex_string = '0'+hex_string
			
		ints = [int(hex_string[i:i+2], 16) for i in range(0,len(hex_string),2)]
		return struct.pack('B' * len(ints), *ints)
		
	tempFile = open(directory+file2)
	tempData = tempFile.read()
	print len(tempData)
	
	tempData = tempData[14:]
	tempData = tempData[:len(tempData)-(2*X)]
	print len(tempData)
	
	endList = [] # tempFile will be read, and the bits needed will be stored here
	endFile = ''
	
	tempX = 1
	charNumber = 1
	
	if (file2 == 'Cror.map'):
		for i in range(len(tempData)): # Cuts the file up into relevant sections (a list of numbers)
			if (i % 2 == 0):
				if (i % X == 0):
					print 'yay'
					pass
				else: # formula for resources: ore = number/2      ec = number+1/2
					if (int('0x'+tempData[i].encode("hex"), 0) == 0): # None
						something = to_binary(hex(0))
						
					elif (int('0x'+tempData[i].encode("hex"), 0) == 1) or (int('0x'+tempData[i].encode("hex"), 0) == 3): # 1 energy crystal
						something = to_binary(hex(1))
						
					elif (int('0x'+tempData[i].encode("hex"), 0) == 2) or (int('0x'+tempData[i].encode("hex"), 0) == 4): # 1 ore
						something = to_binary(hex(2))
						
					elif (int('0x'+tempData[i].encode("hex"), 0) == 5) or (int('0x'+tempData[i].encode("hex"), 0) == 7): # 3 energy crystals
						something = to_binary(hex(5))
						
					elif (int('0x'+tempData[i].encode("hex"), 0) == 6) or (int('0x'+tempData[i].encode("hex"), 0) == 8): # 3 ore
						something = to_binary(hex(6))
						
					elif (int('0x'+tempData[i].encode("hex"), 0) == 9) or (int('0x'+tempData[i].encode("hex"), 0) == 11): # 5 energy crystals
						something = to_binary(hex(9))
						
					elif (int('0x'+tempData[i].encode("hex"), 0) == 10) or (int('0x'+tempData[i].encode("hex"), 0) == 12) or (int('0x'+tempData[i].encode("hex"), 0) == 16): # 5 ore
						something = to_binary(hex(10))
						
					elif (int('0x'+tempData[i].encode("hex"), 0) == 13) or (int('0x'+tempData[i].encode("hex"), 0) == 19): # 11 energy crystals
						something = to_binary(hex(21))
						
					elif (int('0x'+tempData[i].encode("hex"), 0) == 14) or (int('0x'+tempData[i].encode("hex"), 0) == 20): # 11 ore
						something = to_binary(hex(22))
						
					elif (int('0x'+tempData[i].encode("hex"), 0) == 17) or (int('0x'+tempData[i].encode("hex"), 0) == 23): # 25 energy crystals
						something = to_binary(hex(49))
						
					elif (int('0x'+tempData[i].encode("hex"), 0) == 18) or (int('0x'+tempData[i].encode("hex"), 0) == 24): # 25 ore
						something = to_binary(hex(50))
						
					else:
						something = to_binary(hex(int('0x'+tempData[i].encode("hex"), 0)))
					endList.append(something)
				#print len(endList)
	else:
		for i in range(len(tempData)): # Cuts the file up into relevant sections (a list of numbers)
			if (i % 2 == 0):
				if (i % X == 0):
					pass
				else:
					something = to_binary(hex(int('0x'+tempData[i].encode("hex"), 0)))
					endList.append(something)
					#print something, tempData[i]
	
	for value in endList:
		endFile = endFile+str(value)
		
	print len(endFile)
	
	return endFile
	
def makeFile(fileData, name):
	directory2 = directory+'converted/'
	
	if (not os.path.exists(directory2)):
		os.makedirs(directory2)
		
	newFileDir = open(directory2+name, "w")
	print len(newFile)
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
