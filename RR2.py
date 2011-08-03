import Parser
import mapLoader
import modelLoader
import gameMain
import stratCam

parserClass = Parser.Parser()

mapLoaderClass = mapLoader.mapLoader(parserClass)

modelLoaderClass = modelLoader.modelLoader(parserClass, mapLoaderClass)#, mapLoaderClass.mapConfigParser.get("map", "width"))

gameMain = gameMain.world(parserClass, mapLoaderClass, modelLoaderClass)

stratCam.CameraHandler()

run()