import config
import stratCam
import main

startMap = config.parser.getpath("main", "testing_map") # CHECK THE CONFIG FOR THE STARTING MAP!
world = main.world(startMap)
stratCam.CameraHandler()
run()

