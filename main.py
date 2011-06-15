from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import AmbientLight, DirectionalLight
from pandac.PandaModules import VBase4, VBase3
import direct.directbase.DirectStart

class world(DirectObject):
	def __init__(self, mapData):
		#print mapData
		
		models = []
		
		tileX = 0
		tileY = 0
		
		for row in mapData:
			print len(row)
			print row
			for tile in row:
				print dir(tile)
				#model = tile.model
				#tile.model.setPos(tile.posX, tile.posY, 0)
				#tile.model.reparentTo(render)
				#tex=loader.loadTexture(tile.texture)
				#print tex
				#tile.model.setTexture(tex, 1)
				#models.append(tile.model)
				#print tile.name, tile.posX, tile.posY, 0
		
		self.loadLight()
			
	def loadLight(self): #Sets the lights
		plight = AmbientLight('my plight')
		plight.setColor(VBase4(1.0,1.0,1.0,0.5))
		plnp = render.attachNewNode(plight)
		render.setLight(plnp)