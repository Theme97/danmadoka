import pygame, sys
from pygame.locals import *

class player(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.image.load('./homura.png')
		self.image = self.image.convert()
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
	def __init__(self, pos, health, sprite, msUntilSpawn, LevelStart):
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.pos = pos
		self.health = health
		self.sprite = sprite
		self.msUntilSpawn = msUntilSpawn
		self.LevelStart = LevelStart
	def update(self):
		currentTime = pygame.time.get_ticks()
		if currentTime >= self.LevelStart+self.msUntilSpawn:
			activeEnemies(self.pos, self.health, self.sprite)
			self.kill()

class activeEnemies(pygame.sprite.Sprite):
	def __init__(self, pos, health, sprite):
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.image.load(sprite)
		self.image = self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.health = health
	def update(self):
		if pygame.sprite.spritecollideany(self, playerbullets):
			playerBullet.hit(pygame.sprite.spritecollideany(self, playerbullets))
			self.health -= bulletDamage
			if self.health <= 0:
				self.kill()

def level1():
	levelstart = pygame.time.get_ticks()
	Enemy((300,250), 30, "./enemy1.png", 0, levelstart)
	Enemy((250, 100), 60, "./enemy1.png", 1000, levelstart)
	Enemy((100,100), 20, "./enemy1.png", 2000, levelstart)
	Enemy((200,150), 50, "./enemy1.png", 5000, levelstart)

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
playerPosition = (resX/20+fieldwidth/2-resX/50, resY-(fieldheight/10+resY/30+resY/12)) # where player starts

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

	window.fill((0, 0, 0))
	pygame.draw.rect(window, (255, 255, 255), field)

	playergroup.update()
	playerbullets.update()
	inactiveEnemies.update()
	enemies.update()
	playerbullets.draw(window)
	enemies.draw(window)
	playergroup.draw(window)

	pygame.display.update()
	clock.tick(60)