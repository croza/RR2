import config
import stratCam
import main

import basicMoving

startMap = config.parser.getpath("main", "testing_map") # CHECK THE CONFIG FOR THE STARTING MAP!
world = main.world(startMap)
#moving = basicMoving.basicMoving()
stratCam.CameraHandler()
run()

