import base

class level:
	def __init__(self, area):
		self.area = area
	
	def tick(self, time):
		pass

class l1(level):
	def tick(self, time):
		e = base.enemy(self, (50, 50), 100, './img/enemy1.png')
		e.moveCatmullRom([(50, 400), (400, 400)], 300)
		self.area.enemies.add(e)
		e = base.enemy(self, (50, 50), 100, './img/enemy1.png')
		e.moveBezier([(400, 50), (400, 400)], 300)
		self.area.enemies.add(e)
		e = base.enemy(self, (50, 50), 100, './img/enemy1.png')
		e.moveLinear2((400, 400), 300, 4)
		self.area.enemies.add(e)
