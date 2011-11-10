import pygame

class BasePlayer(pygame.sprite.Sprite):
	def __init__(self, game, image):
		# super
		super(BasePlayer, self).__init__()
		
		self.game = game
		self.image = pygame.image.load(image).convert()
		self.rect = self.image.get_rect()
		
		# defaults
		self.speed = (4, 2) # (regular, focused)
		self.radius = 2     # radius (in pixels) of hitbox, always centered
	
	def update(self):
		# move (if applicable)
		self.move()
		
		# check collisions
		for enemy in pygame.sprite.spritecollide(self, self.game.area.enemies, False):
			print enemy
	
	def move(self):
		game = self.game
		if game.keyPressed('left'):
			self.rect.left -= self.getSpeed()
			if self.rect.left < 0: self.rect.left = 0
		if game.keyPressed('up'):
			self.rect.top -= self.getSpeed()
			if self.rect.top < 0: self.rect.top = 0
		if game.keyPressed('right'):
			self.rect.right += self.getSpeed()
			if self.rect.right > 480: self.rect.right = 480
		if game.keyPressed('down'):
			self.rect.bottom += self.getSpeed()
			if self.rect.bottom > 560: self.rect.bottom = 560
	
	def getPos(self): return self.rect.center
	def getSpeed(self): return self.speed[self.game.keyPressed('focus')]

class Homura(BasePlayer):
	def __init__(self, game) :
		super(Homura, self).__init__(game, './homura.png')
		self.speed = (5, 2.5)
