import pygame, base

##########
# Homura #
##########
class Homura(base.player):
	def __init__(self, game):
		super(Homura, self).__init__(game, './img/homura.png')
		self.speed = (5, 2.5)

class HomuraBullet(base.bullet):
	def __init__(self, game):
		super(HomuraBullet, self).__init__(game, './img/hom-bulleta.png')