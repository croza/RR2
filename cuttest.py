x = '1111111111110000000011100000000111000000001110000000011100000000111000000001110000000011100000000111111111111110000000011'
tempX = []

sizeX = 11
currentStr = 0
difference = 1

for i in x:
	if (difference % sizeX == 0):
		#tempX = x[:currentStr]+x[currentStr+1:]
		difference = 1
	else:
		tempX.append(i)
		difference += 1
	currentStr += 1
	
m = str(tempX)
print m, len(tempX)