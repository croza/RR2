import Parser
import mapLoader
import modelLoader
import main
import stratCam

# class world:
	# def __init__(self):
config = Parser.config()

list = mapLoader.mapLoader('data/maps/ten/').generate_tile_array(config)
#print list, len(list)
m = modelLoader.modelLoader(list)
#print m.mapList[1][1].model

l = main.world(m.mapList)

stratCam.CameraHandler()

run()

#w = world()