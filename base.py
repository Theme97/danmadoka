import pygame, motion

##########
# bullet #
##########
class bullet(pygame.sprite.Sprite):
	def __init__(self, game, image):
		# super
		super(base, self).__init__()
		
		self.game = game
		self.image = pygame.image.load(image).convert()
		self.rect = self.image.get_rect()
		
		# defaults
		self.speed = 0
		self.motion = None
		self.radius = 1
	
	def update(self):
		# move (if applicable)
		if isinstance(self.motion, motion.base):
			self.setPos(self.motion.tick())
		
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

#########
# enemy #
#########
class enemy(pygame.sprite.Sprite):
	def __init__(self, game, pos, health, image):
		super(enemy, self).__init__()
		
		self.game = game
		
		self.image = pygame.image.load(image).convert()
		self.rect = self.image.get_rect()
		self.setPos(pos)
		
		self.health = health
		self.motion = None
	
	def update(self):
		if self.motion:
			pos = self.motion.tick()
			self.setPos(pos)
	
	def getPos(self): return self.rect.center
	def setPos(self, pos): self.rect.center = pos
	
	def moveBezier(self, path, frames): self.motion = motion.bezier([self.getPos()] + path, frames)
	def moveLinear(self, pos, frames): self.motion = motion.lerp(self.getPos(), pos, frames)
	def moveLinear2(self, pos, frames, weight): self.motion = motion.bezier([self.getPos()] * weight + [pos] * weight, frames)

##########
# player #
##########
class player(pygame.sprite.Sprite):
	def __init__(self, game, image):
		# super
		super(player, self).__init__()
		
		self.game = game
		self.image = pygame.image.load(image).convert()
		self.rect = self.image.get_rect()
		
		# defaults
		self.speed = (4, 2) # (regular, focused)
		self.radius = 2     # radius (in pixels) of hitbox, always centered
	
	def update(self):
		# move (if applicable)
		self.move()
		
		# shoot (if applicable)
		if self.game.keyPressed('shoot'): self.shoot()
		
		# check collisions
		# TODO: ... collide
		for enemy in pygame.sprite.spritecollide(self, self.game.area.enemies, False):
			print enemy
	
	def move(self):
		game = self.game
		x = game.keyPressed('right') - game.keyPressed('left')
		y = game.keyPressed('down')  - game.keyPressed('up')
		if x and y:
			x *= 0.7071
			y *= 0.7071
		if x:
			self.rect.left += x * self.getSpeed()
			if self.rect.left < 0: self.rect.left = 0
			if self.rect.right > 480: self.rect.right = 480
		if y:
			self.rect.top += y * self.getSpeed()
			if self.rect.top < 0: self.rect.top = 0
			if self.rect.bottom > 560: self.rect.bottom = 560
	
	def shoot(self):
		# subclass should be implementing this
		pass
	
	def setPos(self, pos): self.rect.center = pos
	def getPos(self): return self.rect.center
	def getSpeed(self): return self.speed[self.game.keyPressed('focus')]
