import config
import stratCam
import main

import moving2

startMap = config.parser.getpath("main", "testing_map") # CHECK THE CONFIG FOR THE STARTING MAP!
world = main.world(startMap)
moving = moving2.HeightMoving()
stratCam.CameraHandler()
run()

