from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import AmbientLight, DirectionalLight
from pandac.PandaModules import VBase4, VBase3
import direct.directbase.DirectStart

class world(DirectObject):
	def __init__(self, mapData):
		# <stuff should go here>
		self.loadLight()
		
		print 'END OF MAIN!'
			
	def loadLight(self): #Sets the lights
		plight = AmbientLight('my plight')
		plight.setColor(VBase4(1.0,1.0,1.0,0.5))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)