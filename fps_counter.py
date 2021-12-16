class FPSCounter:
	"""
	FPS counter that stores average value over time period
	"""
	def __init__(self, capacity=30, update_period=1.0):
		self.capacity = capacity
		self.values = [0 for _ in range(0, capacity)]
		self.counter = 0
		self.update_period = update_period
		self.time_passed = 0
		self.avg_fps = 0

	def update(self, dt):
		if dt > 0.0:
			if self.counter == self.capacity - 1:
				self.counter = 0
			self.counter += 1
			self.values[self.counter] = 1.0 / dt
			self.time_passed += dt

	def get_fps(self):
		if self.time_passed > self.update_period:
			self.avg_fps = sum(self.values) / self.capacity
			self.time_passed = 0
		# Returns rounded value
		return int(self.avg_fps)