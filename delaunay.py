
import numpy as np

class Delaunay:
	def __init__(self, center=(0,0), radius=1000): # Constructor
		self.center = np.asarray(center)

		# Initialize a list of the bounding box coordinates initially. This list will be added to later on.
		self.coords = [center+radius*np.array((-1, -1)), center+radius*np.array((+1, -1)), center+radius*np.array((+1, +1)), center+radius*np.array((-1, +1))]

		# Now just initialize the triangle neighbours and circumcircles.
		self.triangles = {}
		self.circles = {}

		T1 = (0,1,3)
		T2 = (2,3,1)

		self.triangles[T1] = [T2, None, None]
		self.triangles[T2] = [T1, None, None]

		# Compute circumcenters and circumradius for each tri
		for tri in self.triangles:
			self.circles[tri] = self.circumcenter(tri)

	def circumcenter(self, triangle):
		'''
		p_0 = (((a_0 - c_0) * (a_0 + c_0) + (a_1 - c_1) * (a_1 + c_1)) / 2 * (b_1 - c_1) 
		    -  ((b_0 - c_0) * (b_0 + c_0) + (b_1 - c_1) * (b_1 + c_1)) / 2 * (a_1 - c_1)) 
		    / D

		p_1 = (((b_0 - c_0) * (b_0 + c_0) + (b_1 - c_1) * (b_1 + c_1)) / 2 * (a_0 - c_0)
		    -  ((a_0 - c_0) * (a_0 + c_0) + (a_1 - c_1) * (a_1 + c_1)) / 2 * (b_0 - c_0))
		    / D

		where D = (a_0 - c_0) * (b_1 - c_1) - (b_0 - c_0) * (a_1 - c_1)

		The _squared_ circumradius is then:

		r^2 = (c_0 - p_0)^2 + (c_1 - p_1)^2
		'''
		print("Here is the triangle: "+str(triangle))
		pts = np.asarray([self.coords[v] for v in triangle])
		print(pts)
		assert len(pts) == 3 # Triangle should have three points.
		a = pts[0]
		b = pts[1]
		c = pts[2]
		a_0 = a[0]
		a_1 = a[1]
		b_0 = b[0]
		b_1 = b[1]
		c_0 = c[0]
		c_1 = c[1]

		D = (a_0 - c_0) * (b_1 - c_1) - (b_0 - c_0) * (a_1 - c_1)
		print("Value of D: "+str(D))
		p_0 = (((a_0 - c_0) * (a_0 + c_0) + (a_1 - c_1) * (a_1 + c_1)) / 2 * (b_1 - c_1) -  ((b_0 - c_0) * (b_0 + c_0) + (b_1 - c_1) * (b_1 + c_1)) / 2 * (a_1 - c_1)) / D
		p_1 = (((b_0 - c_0) * (b_0 + c_0) + (b_1 - c_1) * (b_1 + c_1)) / 2 * (a_0 - c_0) -  ((a_0 - c_0) * (a_0 + c_0) + (a_1 - c_1) * (a_1 + c_1)) / 2 * (b_0 - c_0)) / D
		print("p_0 == "+str(p_0))
		print("p_1 == "+str(p_1))

		distance_squared = (c_0 - p_0)**2 + (c_1 - p_1)**2
		print("distance_squared == "+str(distance_squared))
		return 

