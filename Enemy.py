import pygame
from Motion import *

class Enemy(pygame.sprite.Sprite):
	def __init__(self, game, pos, health, image):
		super(Enemy, self).__init__()
		
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
	
	def moveLinear(self, pos, frames): self.motion = Motion(MOTION_LINEAR, self.getPos(), pos, frames)
	def moveBezier(self, path, frames): self.motion = Motion(MOTION_BEZIER, self.getPos(), path, frames)
	
	def moveLinear2(self, pos, frames, weight):
		orig = self.getPos()
		self.motion = Motion(MOTION_BEZIER, orig, [orig] * (weight - 1) + [pos] * weight, frames)
