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
		self._delayed = 0
		self.image = image
		
		# defaults
		self.rect = image.get_rect()
		self.speed = 0
		self.accel = 0
		
		self.angle = 0
		self.angle_vel = 0
		self.angle_accel = 0
		
		self.dmg = 0
		self.delay = 0
		self.radius = 0
	
	def hit(self, victim):
		self.kill()
		return self.dmg
	
	def update(self):
		if self._delayed < self.delay:
			self.image.set_alpha(float(self._delayed) / self.delay * 255)
			self._delayed += 1
		else:
			# calc angle
			self.angle_vel += self.angle_accel
			self.angle += self.angle_vel
			ang = math.radians(self.angle)
			
			# calc pos
			# TODO: speed_limit
			self.speed += self.accel
			self.rect.move_ip(-math.cos(ang) * self.speed, -math.sin(ang) * self.speed)
			
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
		self.invuln = False
		self.motion = None
	
	def update(self):
		if self.motion: self.rect.center = self.motion.tick()
		
		if self.invuln > 0:
			if self.invuln is not True: self.invuln -= 1
		else:
			self.checkCollision()
	
	def checkCollision(self):
		bullets = pygame.sprite.spritecollide(self, self.game.area.playerBullets, False)
		for bullet in bullets:
			self.health -= bullet.hit(self)
			if self.health < 1:
				self.kill()
				break
	
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
		self.move()
		if self.game.keyPressed('shoot'): self.shoot()
		self.checkCollisions()
	
	def move(self):
		game = self.game
		rect = self.rect
		x = game.keyPressed('right') - game.keyPressed('left')
		y = game.keyPressed('down')  - game.keyPressed('up')
		if x and y:
			x *= 0.7071
			y *= 0.7071
		if x:
			rect.left += x * self.getSpeed()
			if rect.left < 0: rect.left = 0
			if rect.right > 480: rect.right = 480
		if y:
			rect.top += y * self.getSpeed()
			if rect.top < 0: rect.top = 0
			if rect.bottom > 560: rect.bottom = 560
	
	def shoot(self):
		# subclass should be implementing this
		pass
	
	def checkCollisions(self):
		# TODO: ... collide
		for enemy in pygame.sprite.spritecollide(self, self.game.area.enemies, False):
			print enemy
	
	def setPos(self, pos): self.rect.center = pos
	def getPos(self): return self.rect.center
	def getSpeed(self): return self.speed[self.game.keyPressed('focus')]
