########
# base #
########
class base:
	def tick(self): return (0, 0)

########
# lerp #
########
class lerp(base):
	def __init__(self, a, b, frames):
		self.a = a
		self.b = b
		self.frame = 0.0
		self.length = int(frames)
	
	def tick(self):
		if self.frame >= self.length: return self.b
		self.frame += 1
		return self.calc(self.a, self.b, self.frame / self.speed)
	
	@staticmethod
	def calc(a, b, t):
		return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))

##########
# bezier #
##########
class bezier(base):
	def __init__(self, points, frames):
		self.points = points
		self.frame  = 0.0
		self.length = int(frames)
	
	def tick(self):
		if self.frame >= self.length: return self.points[-1]
		self.frame += 1
		return self.calc(self.points, self.frame / self.length)
	
	@staticmethod
	def calc(p, t): # p is a list of (x, y) tuples
		size = len(p)
		if size > 2:
			p2 = []
			for i in range(size - 1): p2.append(lerp.calc(p[i], p[i + 1], t))
			return lerp.calc(p2[0], p2[1], t) if size == 3 else bezier.calc(p2, t)
		elif size == 2:
			return lerp.calc(p[0], p[1], t)
		elif size == 1:
			return p[0]
