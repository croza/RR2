import Parser
import mapLoader
import modelLoader
import main
import stratCam

config = Parser.config()

list = mapLoader.mapLoader('data/maps/ten/').generate_tile_array(config) # A big list of classes: one for each tile
m = modelLoader.modelLoader(list) # Contains a list of classes, with models for each
l = main.world(m.mapList) # The main

stratCam.CameraHandler() # The camera

run()
