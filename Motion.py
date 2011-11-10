MOTION_NONE   = 0
MOTION_LINEAR = 1
MOTION_BEZIER = 2

class Motion:
	def __init__(self, type, orig, path, speed):
		self.orig = orig
		self.path = path
		self.type = type
		self.frame = 0.0   # current number of frames of movement
		self.speed = speed # defined in total number of frames to finish motion
	
	def tick(self):
		""" Calculate coordinates of next position. """
		
		# if no motion, stay at origin
		if self.type == MOTION_NONE: return self.orig
		
		# tick
		pos = self.orig
		self.frame += 1
		if self.type == MOTION_LINEAR: pos = self._linear(pos, self.path, self.frame / self.speed)
		if self.type == MOTION_BEZIER: pos = self._bezier([pos] + self.path, self.frame / self.speed)
		
		# set new origin and disable motion if we're done
		if self.frame >= self.speed:
			self.orig = pos
			self.type = MOTION_NONE
		
		# return new pos
		return pos
	
	#####################
	# movement formulas #
	#####################
	def _linear(self, start, end, t):
		return (start[0] + t * (end[0] - start[0]), start[1] + t * (end[1] - start[1]))
	
	def _bezier(self, path, t):
		size = len(path)
		if size > 2:
			points = []
			for i in range(size - 1): points.append(self._linear(path[i], path[i + 1], t))
			return self._linear(points[0], points[1], t) if size == 3 else self._bezier(points, t)
		elif size == 2:
			return self._linear(path[0], path[1], t)
		else:
			return path[0] if size == 1 else self.orig
