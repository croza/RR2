import config
import stratCam
import main

startMap = config.parser.getpath("main", "testing_map")
world = main.world(startMap)
stratCam.CameraHandler()
run()

