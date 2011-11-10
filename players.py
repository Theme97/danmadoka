import pygame, base

##########
# Homura #
##########
class Homura(base.player):
	def __init__(self, game):
		super(Homura, self).__init__(game, './img/homura.png')
		self.speed = (5, 2.5)
		self.nextShot = 0
	
	def shoot(self):
		if self.nextShot <= self.game.ticks:
			if self.game.keyPressed('focus'):
				self.nextShot = self.game.ticks + 20
				bullet = HomuraBullet(self.game, self.getPos())
				bullet.angle = 105
				self.game.area.addPlayerBullet(bullet)
				bullet = HomuraBullet(self.game, self.getPos())
				bullet.angle = 75
				self.game.area.addPlayerBullet(bullet)
			else:
				self.nextShot = self.game.ticks + 10
				bullet = HomuraBullet(self.game, self.getPos())
				self.game.area.addPlayerBullet(bullet)

class HomuraBullet(base.bullet):
	image = None
	
	def __init__(self, game, pos):
		if not HomuraBullet.image: HomuraBullet.image = pygame.image.load('./img/hom-bulleta.png').convert_alpha()
		super(HomuraBullet, self).__init__(game, HomuraBullet.image)
		self.angle = 90
		self.speed = 10
		self.dmg = 10
		self.rect.center = pos