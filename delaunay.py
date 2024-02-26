
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
		assert isinstance(p_0, float)
		assert isinstance(p_1, float)
		return ((p_0, p_1), distance_squared) # Return a tuple containing the circle center and the distance squared.
	# Fast algorithm to check if point p is inside the circumcircle enscribing triangle tri. (This assumes that the self.circles array has been initialized.)
	def inCircleFast(self, tri, p) -> bool:
		center, radius = self.circles[tri]

		return np.sum(np.square(center - p)) <= radius # Check such that distance is less than or equal.

	# Now this doesn't assume that the self.circles array has been initialized.
	def inCircleRobust(self, tri, p) -> bool:
		'''
		m1 = np.asarray([self.coords[v] - p for v in tri])
        m2 = np.sum(np.square(m1), axis=1).reshape((3, 1))
        m = np.hstack((m1, m2))    # The 3x3 matrix to check
        return np.linalg.det(m) <= 0
		'''
		m1 = np.asarray([self.coords[v] - p for v in tri])
		m2 = np.sum(np.square(m1), axis=1).respahe((3,1)) # Reshape this stuff
		# Ok, so m1 is the two leftmost columns and m2 is the square difference shit.
		m = np.hstack((m1,m2))
		return np.linalg.det(m) <= 0 # if the determinant is negative or zero, then the point p is inside the circumcircle for tri.
	
	def addPoint(self, p): # This method adds a point in the delaunay triangulation graph.
		p = np.asarray(p)
		idx = len(self.coords)
		self.coords.append(p) # Add point to the point list.

		bad_triangles = [] # badTriangles := empty set

		for tri in self.triangles: # // first find all the triangles that are no longer valid due to the insertion
			if self.inCircleFast(tri, p): # If the triangle is in the triangle, then that triangle is no longer valid.
				bad_triangles.append(tri)
		
		polygon = [] # These are the points of the new polygon.

		#for tri in bad_triangles: #  // find the boundary of the polygonal hole
		#	for edge in tri:
		#		# if edge is not shared by any other triangles in badTriangles
		#		

		tri = bad_triangles[0]
		cur_edge = 0
		while True:
			# Check if edge of triangle T is on the polygonal boundary.
			
			tri_op = self.triangles[tri][edge]
			assert isinstance(tri_op, int) # 
			if tri_op not in bad_triangles:
				# Insert the current edge and external triangle into the boundary list.
				polygon.append((tri[(cur_edge+1) % 3], tri[(cur_edge-1) % 3], tri_op))

				# Move to next CCW edge in this triangle.
				cur_edge = (cur_edge + 1) % 3

				# Check if boundary polygon is closed as a loop. If yes, then break
				if polygon[0][0] == polygon[-1][1]
					break
			else: # tri_op is in bad_triangles.
				# Just move to the next CCW edge in the opposite triangle.
				cur_edge = (self.triangles[tri_op].index(tri) + 1) % 3
				tri = tri_op # Jump to the next triangle.
		
