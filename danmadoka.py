# Notes:
# window size is normalized to 800x600
# play area is 480x560 offset by 40x20

import pygame, sys
import base, players, levels

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
		
		self.ticks = 0
		
		area = self.area = PlayArea(self)
		area.setPlayer(players.Homura)
		
		level = self.level = levels.l1(area)
		level.tick(0)
	
	def keyPressed(self, key): return self.keys[self.system.keys[key]]
	
	def update(self):
		self.area.update()
		scale = pygame.transform.scale if self.system.res[0] <= 800 else pygame.transform.smoothscale
		scale(self.window, self._window.get_size(), self._window)
		# TODO: TATE?
		self.ticks += 1

############
# PlayArea #
############
class PlayArea:
	def __init__(self, game):
		# private vars
		self._game = game
		
		# surfaces
		self.rect = pygame.Rect(40, 20, 480, 560)
		self.size = (self.rect.width, self.rect.height)
		self.surface = game.window.subsurface(self.rect)
		
		# groups
		self.player = pygame.sprite.GroupSingle()
		self.playerBullets = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		self.enemyBullets = pygame.sprite.Group()
		self.enemyBulletQueue = pygame.sprite.Group()
		
		# options
		self.setBulletClip((64, 64, 64, 64))
		
		# draw bg
		pygame.display.flip()
	
	def setPlayer(self, player):
		p = player(self._game)
		p.setPos((self.size[0] * 0.5, self.size[1] * 0.9))
		self.player.add(p)
	
	def setBulletClip(self, size):
		self.bulletClip = pygame.Rect(-size[0], -size[1], self.size[0] + size[2], self.size[1] + size[3])
	
	def addPlayerBullet(self, bullet):
		self.playerBullets.add(bullet)
		bullet.Init = True
	
	def update(self):
		# draw bg
		self._game.window.fill((0, 0, 0)) # fill window bg (stage image goes here)
		self.surface.fill((255, 255, 255)) # fill playarea bg (uhhh. stuff goes here)
		
		# update groups
		self.player.update()
		self.playerBullets.update()
		self.enemies.update()
		self.enemyBullets.update()
		self.enemyBulletQueue.update()
		
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
