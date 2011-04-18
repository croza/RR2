import mapLib

tiles = []
for x in range(10):
	for y in range(10):
		tiles.append(mapLib.Tile(x, y, 0, 0, 0))

print tiles

wallData = ""
resData = ""
for tile in tiles:
	wallTile, resTile = tile.toData()
	
	wallData += (wallTile)
	resData += (resTile)

open("wall.map", "w").write(wallData)
open("resource.map", "w").write(resData)
