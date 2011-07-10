import Parser
import mapLoader
from pandac.PandaModules import *
import gameMain
import stratCam



#import libpandaexpress

config = Parser.config()
print config.units[0].model

mapLoad = mapLoader.mapLoader('data/maps/ten/')

list = mapLoad.generate_tile_array(config) # A big list of classes, one for each tile on the map (from classes mad in the parser)
print mapLoad.height

main = gameMain.world(list, config.classes, mapLoad.width, mapLoad.height, config.units) # The main

stratCam.CameraHandler() # The camera

run()
