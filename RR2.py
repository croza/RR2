import config
import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.gui.DirectGui import OnscreenText
from direct.showbase.DirectObject import DirectObject

from stratCam import CameraHandler

# from dev1 import * # Working, but corners are blargh and before the restructure.
import main


startMap = config.parser.getpath("main", "testing_map")
world = main.world(startMap)
#World1()
CameraHandler()
run()

