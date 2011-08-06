import Parser
import mapLoader
import modelLoader
import gameMain
import stratCam
import fpsTest
import something2

parserClass = Parser.Parser()

mapLoaderClass = mapLoader.mapLoader(parserClass)

modelLoaderClass = modelLoader.modelLoader(parserClass, mapLoaderClass)#, mapLoaderClass.mapConfigParser.get("map", "width"))

gameMain = gameMain.world(parserClass, mapLoaderClass, modelLoaderClass)

stratCam.CameraHandler(modelLoaderClass.mapX, modelLoaderClass.mapY,
		parserClass.userConfig.getfloat("control", "scrollborder"),
		parserClass.userConfig.getfloat("control", "zoominspeed"),
		parserClass.userConfig.getfloat("control", "zoomoutspeed"),
		parserClass.userConfig.getfloat("control", "zoommax"),
		parserClass.userConfig.getfloat("control", "zoommin"))

#f = fpsTest.thirdPerson(parserClass, gameMain, mapLoaderClass, modelLoaderClass)
#s = something2.Nodes(mapLoaderClass, 10, 10)

run()