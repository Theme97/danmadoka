import pygame, math, motion

##########
# bullet #
##########
class bullet(pygame.sprite.Sprite):
	def __init__(self, game, image):
		# setup
		super(bullet, self).__init__()
		self._game  = game
		self._image = image
		self.image = image
		
		# defaults
		self.init = False
		
		self.rect = image.get_rect()
		self.speed = 0
		self.accel = 0
		
		self.angle = 0
		self.angle_vel = 0
		self.angle_accel = 0
		
		self.dmg = 0
		self.delay = 0
		self.frame = 0
		self.radius = 0
	
	def update(self):
		if not self.Init: return
		
		rect = self.rect
		
		if self.frame < self.delay:
			self.image.set_alpha(float(self.frame) / self.delay * 255)
			self.frame += 1
		else:
			# calc angle
			self.angle_vel += self.angle_accel
			self.angle += self.angle_vel
			ang = math.radians(self.angle)
			
			# calc pos
			# TODO: figure out what's going wrong here
			rect.center = (rect.center[0] - math.cos(ang) * self.speed, rect.center[1] - math.sin(ang) * self.speed)
			
			# check clip
			if not self._game.area.bulletClip.collidepoint(self.rect.center):
				return self.kill()
			
			# rotate image
			if self.angle_vel: self.image = pygame.transform.rotate(self.image, self.angle_vel)

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
