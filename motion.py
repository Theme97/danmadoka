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
		elif size == 0:
			return (0, 0)

##############
# catmullRom #
##############
class catmullRom(base):
	def __init__(self, points, frames):
		n = len(points) - 1
		self.points = [points[0]] + points + [points[-1]]
		self.frame  = 0.0
		self.step   = n / float(frames)
		self.length = n - self.step
	
	def tick(self):
		if self.frame >= self.length: return self.points[-2]
		self.frame += self.step
		s = int(self.frame)
		return self.calc(self.points[s:s+4], self.frame % 1)
	
	@staticmethod
	def calc(p, t):
		t2 = t * t
		t3 = t2 * t
		m1 = -0.5*t3 +     t2 - 0.5*t
		m2 =  1.5*t3 - 2.5*t2         + 1.0
		m3 = -1.5*t3 + 2.0*t2 + 0.5*t
		m4 =  0.5*t3 - 0.5*t2
		return (m1*p[0][0] + m2*p[1][0] + m3*p[2][0] + m4*p[3][0], m1*p[0][1] + m2*p[1][1] + m3*p[2][1] + m4*p[3][1])
