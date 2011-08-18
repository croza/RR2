import Parser
import mapLoader
import modelLoader
import gameMain
import stratCam
import fpsTest
import astar

parserClass = Parser.Parser()

mapLoaderClass = mapLoader.mapLoader(parserClass)

modelLoaderClass = modelLoader.modelLoader(parserClass, mapLoaderClass)#, mapLoaderClass.mapConfigParser.get("map", "width"))

gameMain = gameMain.world(parserClass, mapLoaderClass, modelLoaderClass)

cameraClass = stratCam.CameraHandler(parserClass, mapLoaderClass, modelLoaderClass, gameMain,
		modelLoaderClass.mapX, modelLoaderClass.mapY,
		parserClass.userConfig.getfloat("control", "scrollborder"),
		parserClass.userConfig.getfloat("control", "zoominspeed"),
		parserClass.userConfig.getfloat("control", "zoomoutspeed"),
		parserClass.userConfig.getfloat("control", "zoommax"),
		parserClass.userConfig.getfloat("control", "zoommin"))

#f = fpsTest.thirdPerson(parserClass, gameMain, mapLoaderClass, modelLoaderClass)
##s = astar.grid(mapLoaderClass)
##s1 = astar.aStar(s.landMesh, mapLoaderClass)
##s1.moveTo((6,34))

#j = stratCam.mouseHandler(parserClass, mapLoaderClass, modelLoaderClass, gameMain)

run()