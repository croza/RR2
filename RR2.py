import Parser
import mapLoader
import modelLoader
import main
import stratCam

config = Parser.config()

list = mapLoader.mapLoader('data/maps/ten/').generate_tile_array(config) # A big list of classes, one for each tile on the map (from classes mad in the parser)

#list = modelLoader.modelLoader(list, config.classes) # A more detailed list, with positions, height and rendered models attached
l = main.world(list, config.classes) # The main

stratCam.CameraHandler() # The camera

run()
