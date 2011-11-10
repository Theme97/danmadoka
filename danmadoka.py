# Notes:
# window size is normalized to 800x600
# play area is 480x560 offset by 40x20

import pygame, sys
import players

from Enemy import *

########
# Game #
########
class Game:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption('danmadoka')
		
		system = self.system = System()
		self._window = pygame.display.set_mode(system.res, 0, 32)
		
		self.keys   = pygame.key.get_pressed()
		self.window = pygame.transform.scale(self._window, (800, 600))
		
		area = self.area = PlayArea(self)
		area.setPlayer(players.Homura)
		
		enemy = Enemy(self, (50, 50), 100, './enemy1.png')
		enemy.moveBezier([(50, 400), (400, 50), (400, 400)], 600)
		area.enemies.add(enemy)
		enemy = Enemy(self, (50, 50), 100, './enemy1.png')
		enemy.moveBezier([(400, 50), (50, 400), (400, 400)], 600)
		area.enemies.add(enemy)
		enemy = Enemy(self, (50, 50), 100, './enemy1.png')
		enemy.moveLinear2((400, 400), 600, 2)
		area.enemies.add(enemy)
	
	def keyPressed(self, key): return self.keys[self.system.keys[key]]
	
	def update(self):
		self.area.update()
		pygame.transform.scale(self.window, self._window.get_size(), self._window)
		# TODO: TATE?

##########
# System #
##########
class System:
	def __init__(self):
		# TODO: read from some config file
		self.res = (640, 480)
		self.keys = {
			'left' : pygame.K_LEFT,
			'up'   : pygame.K_UP,
			'down' : pygame.K_DOWN,
			'right': pygame.K_RIGHT,
			'shoot': pygame.K_z,
			'bomb' : pygame.K_x,
			'focus': pygame.K_LSHIFT,
		}

############
# PlayArea #
############
class PlayArea:
	def __init__(self, game):
		# private vars
		self._game = game
		
		# init surfaces
		self.rect = pygame.Rect(40, 20, 480, 560)
		self.surface = game.window.subsurface(self.rect)
		
		# init groups
		self.player = pygame.sprite.GroupSingle()
		self.playerBullets = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		self.enemyBullets = pygame.sprite.Group()
		
		# draw bg
		pygame.display.flip()
	
	def setPlayer(self, player): self.player.add(player(self._game))
	
	def update(self):
		# draw bg
		self._game.window.fill((0, 0, 0)) # fill window bg (stage image goes here)
		self.surface.fill((255, 255, 255)) # fill playarea bg (uhhh. stuff goes here)
		
		# update groups
		self.player.update()
		self.playerBullets.update()
		self.enemies.update()
		self.enemyBullets.update()
		
		# draw groups
		self.playerBullets.draw(self.surface)
		self.enemies.draw(self.surface)
		self.player.draw(self.surface)
		
		# update screen
		pygame.display.update(self.rect)

##########
# main() #
##########
game = Game()
clock = pygame.time.Clock()
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()	
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
			game.keys = pygame.key.get_pressed()
	
	game.update()
	clock.tick(60)
