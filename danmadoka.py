import pygame, sys
from pygame.locals import *

class playerBullet(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.image.load('./hom-bulleta.png') # screen res issue
		self.image = self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.center = pos
		global lastBullet
		lastBullet = pygame.time.get_ticks()
	def update(self):
		self.rect.top -= playerBulletSpeed
		if self.rect.bottom < resY/30:
			self.kill()
		else:
			pygame.draw.rect(self.image, (0, 0, 0), self.rect)
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
			self.health -= 10
			if self.health <= 0:
				self.kill()

def level1():
	levelstart = pygame.time.get_ticks()
	Enemy((100,100), 20, "./enemy1.png", 2000, levelstart) # screen res issue
	Enemy((200,100), 50, "./enemy1.png", 5000, levelstart)
	Enemy((300,250), 30, "./enemy1.png", 0, levelstart)

# Size config #		
resX = 640
resY = 480
playerwidth = 3*resX/80 # 24 @ 640
playerheight = resY/12 # 40 @ 480
fieldwidth = 3*resX/5 # 384 @ 640
fieldheight = resY-2*resY/30 # 448 @ 480

# Speed config #
regXspeed = resX/160 # 4 @ 640
regYspeed = resY/120 # 4 @ 480
focusXspeed = resX/320 # 2 @ 640
focusYspeed = resY/240 # 2 @ 480
playerBulletSpeed = resY/60 # 8 @ 480

# Misc. config #
msBetweenShots = 150
playerstartX = resX/20+fieldwidth/2-resX/50
playerstartY = resY-(fieldheight/10+resY/30+playerheight)

# Stuff #
goUp = False
goDown = False
goLeft = False
goRight = False
shooting = False
lastBullet = 0
playerXspeed = regXspeed
playerYspeed = regYspeed

#biggroup = pygame.sprite.LayeredUpdates()

playerbullets = pygame.sprite.Group()
playerBullet.groups = playerbullets#, biggroup

inactiveEnemies = pygame.sprite.Group()
Enemy.groups = inactiveEnemies#, biggroup

enemies = pygame.sprite.Group()
activeEnemies.groups = enemies#, biggroup

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('danmadoka')
window = pygame.display.set_mode((resX, resY), 0, 32)

field = pygame.Rect(resX/20, resY/30, fieldwidth, fieldheight)
player = pygame.Rect(playerstartX, playerstartY, playerwidth, playerheight)

level1()

while True:
	window.fill((0, 0, 0))
	pygame.draw.rect(window, (255, 255, 255), field)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()	
		if event.type == KEYDOWN:
			if event.key == K_UP:
				goUp = True
			if event.key == K_DOWN:
				goDown = True
			if event.key == K_LEFT:
				goLeft = True
			if event.key == K_RIGHT:
				goRight = True
			if event.key == K_z:
				shooting = True
			if event.key == K_LSHIFT:
				playerXspeed = focusXspeed
				playerYspeed = focusYspeed
		if event.type == KEYUP:
			if event.key == K_UP or event.key == K_w:
				goUp = False
			if event.key == K_DOWN or event.key == K_s:
				goDown = False
			if event.key == K_LEFT or event.key == K_a:
				goLeft = False
			if event.key == K_RIGHT or event.key == K_d:
				goRight = False
			if event.key == K_z:
				shooting = False
			if event.key == K_LSHIFT:
				playerXspeed = regXspeed
				playerYspeed = regYspeed
	if goUp:
		player.top -= playerYspeed
		if player.top < resY/30:
			player.top = resY/30
	if goDown:
		player.bottom += playerYspeed
		if player.bottom > resY-resY/30:
			player.bottom = resY-resY/30
	if goLeft:
		player.left -= playerXspeed
		if player.left < resX/20:
			player.left = resX/20
	if goRight:
		player.right += playerXspeed
		if player.right > resX/20+fieldwidth:
			player.right = resX/20+fieldwidth
	if shooting:
		currentTime = pygame.time.get_ticks()
		if currentTime > lastBullet+msBetweenShots:
			playerBullet(player.center)

	playerbullets.update()
	playerbullets.draw(window)
	inactiveEnemies.update()
	enemies.update()
	enemies.draw(window)
	window.blit(pygame.image.load('./homura.png'), player)

	pygame.display.update()
	clock.tick(60)
