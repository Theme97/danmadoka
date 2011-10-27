import pygame, sys
from pygame.locals import *

class player(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.image.load('./homura.png')
		self.image = self.image.convert()
		self.image = scaleImage(self.image)
		self.rect = self.image.get_rect()
		self.rect.center = pos
	def update(self):
		if keys[keyUp]:
			self.rect.top -= playerYspeed
			if self.rect.top < resY/30:
				self.rect.top = resY/30
		if keys[keyDown]:
			self.rect.bottom += playerYspeed
			if self.rect.bottom > resY-resY/30:
				self.rect.bottom = resY-resY/30
		if keys[keyLeft]:
			self.rect.left -= playerXspeed
			if self.rect.left < resX/20:
				self.rect.left = resX/20
		if keys[keyRight]:
			self.rect.right += playerXspeed
			if self.rect.right > resX/20+fieldwidth:
				self.rect.right = resX/20+fieldwidth
		global playerPosition
		playerPosition = self.rect.center

class playerBullet(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.image.load('./hom-bulleta.png')
		self.image = scaleImage(self.image)
		self.image = self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.center = pos
		global lastBullet
		lastBullet = pygame.time.get_ticks()
	def update(self):
		self.rect.top -= playerBulletSpeed
		if self.rect.bottom < resY/30:
			self.kill()		
	def hit(self):
		self.kill()

class Enemy(pygame.sprite.Sprite):
	def __init__(self, PointA_x, PointA_y, PointB_x, PointB_y, speed, health, sprite, msUntilSpawn, LevelStart):
		pygame.sprite.Sprite.__init__(self, self.groups)
		PointA_x = resX/640*PointA_x
		PointA_y = resY/480*PointA_y
		PointB_x = resX/640*PointB_x
		PointB_y = resY/480*PointB_y
		self.PointA_x = PointA_x
		self.PointA_y = PointA_y
		self.PointB_x = PointB_x
		self.PointB_y = PointB_y 
		self.speed = speed/60
		self.health = health
		self.sprite = sprite
		self.msUntilSpawn = msUntilSpawn
		self.LevelStart = LevelStart
	def update(self):
		currentTime = pygame.time.get_ticks()
		if currentTime >= self.LevelStart+self.msUntilSpawn:
			activeEnemies(self.PointA_x, self.PointA_y, self.PointB_x, self.PointB_y, self.speed, self.health, self.sprite)
			self.kill()

class activeEnemies(pygame.sprite.Sprite):
	def __init__(self, PointA_x, PointA_y, PointB_x, PointB_y, speed, health, sprite):
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.image.load(sprite)
		self.image = self.image.convert()
		self.image = scaleImage(self.image)
		self.rect = self.image.get_rect()
		self.PointA_x = PointA_x
		self.PointA_y = PointA_y
		self.PointB_x = PointB_x
		self.PointB_y = PointB_y
		self.speed = speed
		self.health = health
		self.t = 0
	def update(self):
		if pygame.sprite.spritecollideany(self, playerbullets):
			playerBullet.hit(pygame.sprite.spritecollideany(self, playerbullets))
			self.health -= bulletDamage
			if self.health <= 0:
				self.kill()
		self.rect.right = self.PointA_x+self.t*(self.PointB_x-self.PointA_x)
		self.rect.bottom = self.PointA_y+self.t*(self.PointB_y-self.PointA_y)	
		self.t += self.speed
		if self.t >= 1:
			self.kill()

def scaleImage(image):
	width = image.get_width()
	height = image.get_height()
	scaledimage = pygame.transform.scale(image, (resX/640*width, resY/480*height))
	return scaledimage

def level1():
	levelstart = pygame.time.get_ticks()
	# (PointA_x, PointA_y, PointB_x, PointB_y, speed, health, sprite, msUntilSpawn, LevelStart)
	Enemy(0, 300, 300, 0, 0.4, 30, "./enemy1.png", 3000, levelstart)
	Enemy(0, 200, 500, 200, 0.1, 40, "./enemy1.png", 500, levelstart)
	Enemy(500, 300, 0, 300, 0.1, 40, "./enemy1.png", 500, levelstart)

pygame.init()

# Player config. #
resX = 640
resY = 480
keyUp = K_UP
keyDown = K_DOWN
keyLeft = K_LEFT
keyRight = K_RIGHT
keyShoot = K_z
keyBomb = K_x # this will do something one day I promise
keyFocus = K_LSHIFT

# Size #
fieldwidth = 3*resX/5 # 384 @ 640
fieldheight = resY-2*resY/30 # 448 @ 480

# Speed #
regXspeed = resX/160 # 4 @ 640
regYspeed = resY/120 # 4 @ 480
focusXspeed = resX/320 # 2 @ 640
focusYspeed = resY/240 # 2 @ 480
playerBulletSpeed = resY/60 # 8 @ 480

# Misc. #
msBetweenShots = 150
regbulletDamage = 10
focusbulletDamage = 20
playerPosition = (fieldwidth/2+resX/20, 9*fieldheight/10+resY/30) # where player starts

# Stuff #
clock = pygame.time.Clock()
pygame.display.set_caption('danmadoka')
window = pygame.display.set_mode((resX, resY), 0, 32)
keys = pygame.key.get_pressed()
lastBullet = 0

# Groups #
playergroup = pygame.sprite.Group()
player.groups = playergroup

playerbullets = pygame.sprite.Group()
playerBullet.groups = playerbullets

inactiveEnemies = pygame.sprite.Group()
Enemy.groups = inactiveEnemies

enemies = pygame.sprite.Group()
activeEnemies.groups = enemies

field = pygame.Rect(resX/20, resY/30, fieldwidth, fieldheight)
marginleft = pygame.Rect(0, 0, resX/20, resY)
marginright = pygame.Rect(fieldwidth+resX/20, 0, resX-(fieldwidth+resX/20), resY)
margintop = pygame.Rect(resX/20, 0, fieldwidth, resY/30)
marginbottom = pygame.Rect(resX/20, resY/30+fieldheight, fieldwidth, resY/30)

player(playerPosition)

level1()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()	
		if event.type == KEYDOWN or event.type == KEYUP:
			keys = pygame.key.get_pressed()

	bulletDamage = regbulletDamage
	playerXspeed = regXspeed
	playerYspeed = regYspeed

	if keys[keyFocus]:
		bulletDamage = focusbulletDamage
		playerXspeed = focusXspeed
		playerYspeed = focusYspeed
	if keys[keyShoot]:
		currentTime = pygame.time.get_ticks()
		if currentTime > lastBullet+msBetweenShots:
			playerBullet(playerPosition)

	pygame.draw.rect(window, (255, 255, 255), field)

	playergroup.update()
	playerbullets.update()
	inactiveEnemies.update()
	enemies.update()
	playerbullets.draw(window)
	enemies.draw(window)
	playergroup.draw(window)

	# try to optimize. pygame.transform.chop? #
	pygame.draw.rect(window, (0, 0, 0), marginleft)
	pygame.draw.rect(window, (0, 0, 0), marginright)
	pygame.draw.rect(window, (0, 0, 0), margintop)
	pygame.draw.rect(window, (0, 0, 0), marginbottom)

	pygame.display.update()
	clock.tick(60)
