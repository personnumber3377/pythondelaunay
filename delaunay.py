
import numpy as np

class Delaunay:
	def __init__(self, center=(0,0), radius=1000): # Constructor
		self.center = np.asarray(center)

		# Initialize a list of the bounding box coordinates initially. This list will be added to later on.
		self.coord = [center+radius*np.array((-1, -1)), center+radius*np.array((+1, -1)), center+radius*np.array((+1, +1)), center+radius*np.array((-1, +1))]

		# Now just initialize the triangle neighbours and circumcircles.
		self.triangles = {}
		self.circles = {}

		



