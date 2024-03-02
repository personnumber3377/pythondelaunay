
import numpy as np
import math
import time
EXCEPTION = False
from util import *



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
		#print("Here is the triangle: "+str(triangle))
		pts = np.asarray([self.coords[v] for v in triangle])
		#print(pts)
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
		#print("Value of D: "+str(D))
		
		# This bounds check is ripped straight from here: https://github.com/d3/d3-delaunay/blob/main/src/voronoi.js
		'''
		if (Math.abs(ab) < 1e-9) {
			// For a degenerate triangle, the circumcenter is at the infinity, in a
			// direction orthogonal to the halfedge and away from the “center” of
			// the diagram <bx, by>, defined as the hull’s barycenter.
			if (bx === undefined) {
			bx = by = 0;
			for (const i of hull) bx += points[i * 2], by += points[i * 2 + 1];
			bx /= hull.length, by /= hull.length;
			}
			const a = 1e9 * Math.sign((bx - x1) * ey - (by - y1) * ex);
			x = (x1 + x3) / 2 - a * ey;
			y = (y1 + y3) / 2 + a * ex;
		} else {
		'''

		if D <= 10**(-9):
			D = 0.01 # Just force it


		p_0 = (((a_0 - c_0) * (a_0 + c_0) + (a_1 - c_1) * (a_1 + c_1)) / 2 * (b_1 - c_1) -  ((b_0 - c_0) * (b_0 + c_0) + (b_1 - c_1) * (b_1 + c_1)) / 2 * (a_1 - c_1)) / D
		p_1 = (((b_0 - c_0) * (b_0 + c_0) + (b_1 - c_1) * (b_1 + c_1)) / 2 * (a_0 - c_0) -  ((a_0 - c_0) * (a_0 + c_0) + (a_1 - c_1) * (a_1 + c_1)) / 2 * (b_0 - c_0)) / D
		#print("p_0 == "+str(p_0))
		#print("p_1 == "+str(p_1))

		distance_squared = (c_0 - p_0)**2 + (c_1 - p_1)**2
		#print("distance_squared == "+str(distance_squared))
		assert isinstance(p_0, float)
		assert isinstance(p_1, float)
		assert p_0 != math.nan
		assert p_0 != math.inf
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
		m2 = np.sum(np.square(m1), axis=1).reshape((3,1)) # Reshape this stuff
		# Ok, so m1 is the two leftmost columns and m2 is the square difference shit.
		m = np.hstack((m1,m2))
		return np.linalg.det(m) <= 0 # if the determinant is negative or zero, then the point p is inside the circumcircle for tri.
	
	def addPoint(self, p): # This method adds a point in the delaunay triangulation graph.
		p = np.asarray(p)
		idx = len(self.coords)
		self.coords.append(p) # Add point to the point list.

		bad_triangles = [] # badTriangles := empty set
		found = False
		for tri in self.triangles: # // first find all the triangles that are no longer valid due to the insertion
			#if self.inCircleFast(tri, p): # If the triangle is in the triangle, then that triangle is no longer valid.
			if self.inCircleFast(tri, p):
				print("We found the bad triangle!!!!")
				found = True
				bad_triangles.append(tri)
		
		assert found # There should atleast be one bad triangle.


		polygon = [] # These are the points of the new polygon.

		#for tri in bad_triangles: #  // find the boundary of the polygonal hole
		#	for edge in tri:
		#		# if edge is not shared by any other triangles in badTriangles
		#		
		if len(bad_triangles) == 0: # fuck!
			self.coords.pop(-1) # Revert the adding of the very last element
			assert False # Fuuuccccckkkk
			return
		
		tri = bad_triangles[0]
		cur_edge = 0

		#  This variable is to see if we find a polygon or not.
		found_polygon = False

		while True:
			# Check if edge of triangle T is on the polygonal boundary.
			
			tri_op = self.triangles[tri][cur_edge]
			#print("tri_op == "+str(tri_op))
			#assert isinstance(tri_op, int) # 
			if tri_op not in bad_triangles:
				# Insert the current edge and external triangle into the boundary list.
				polygon.append((tri[(cur_edge+1) % 3], tri[(cur_edge-1) % 3], tri_op))

				# Move to next CCW edge in this triangle.
				cur_edge = (cur_edge + 1) % 3

				# Check if boundary polygon is closed as a loop. If yes, then break
				if polygon[0][0] == polygon[-1][1]:
					found_polygon = True
					break
			else: # tri_op is in bad_triangles.
				# Just move to the next CCW edge in the opposite triangle.
				cur_edge = (self.triangles[tri_op].index(tri) + 1) % 3
				tri = tri_op # Jump to the next triangle.

		# polygon

		render_triangles(bad_triangles, self.coords, color="blue")
		render_points([p], color="purple")
		print("p == "+str(p))
		#print("p.select(0) == "+str(p.select(0)))
		#if p == np.array([-0.06666666666666665, -0.33333333333333337]): # Check for the buggy point.

		#time.sleep(100000)
		removed_shit = set()
		# Remove the "bad" triangles
		for t in bad_triangles:
			if t == tri_op:
				assert False, "Fuck!"
			removed_shit.add(t) # add the triangle to the removed shit set.
			del self.triangles[t]
			del self.circles[t]

		print("Value of found_polygon: "+str(found_polygon))
		self.render_polygon(polygon)

		if (p == np.array([-0.06666666666666665, -0.33333333333333337])).all():
			

			print("Here is the current value of polygon: "+str(polygon))
			print("Here is the removed_shit: "+str(removed_shit))

			# Now render the polygon shit.
			self.render_polygon(polygon)
			#time.sleep(300) # sleep
		
		
		# Retriangle the hole left by bad triangles.
		new_triangles = []
		for (e0, e1, tri_op) in polygon: # e0 is the edge and then the tri_op is the thing.
			# Create a new triangle using point p and edge extremes.
			T = (idx, e0, e1)

			#assert not tri_op in bad_triangles

			# Store the circumcenter and circumradius of the triangle.
			self.circles[T] = self.circumcenter(T)
			# Set opposite triangle of the edge as neigbhour of T
			self.triangles[T] = [tri_op, None, None]

			#print("self.triangles == "+str(self.triangles))

			# Try to set T as neighbour of the opposite triangle
			if tri_op:
				# Search the neighbour of the opposite triangle.
				#print("tri_op in removed_shit: "+str(tri_op in removed_shit))

				'''
				if tri_op not in self.triangles:
					global EXCEPTION
					EXCEPTION = True # Set the exception marker.
					assert False
					return
				'''


				#print("tri_op == "+str(tri_op))

				#render_triangles(tri_op, self.coords, color="blue")

				for i, neigh in enumerate(self.triangles[tri_op]):
					if neigh:
						if e1 in neigh and e0 in neigh:
							# Change link to use our new triangle.
							self.triangles[tri_op][i] = T
			
			# Add triangle to a temporan list
			new_triangles.append(T)
		
		# Link the new triangles each another.
		N = len(new_triangles)
		for i, T in enumerate(new_triangles):
			self.triangles[T][1] = new_triangles[(i+1) % N] # Next
			self.triangles[T][2] = new_triangles[(i-1) % N] # previous.

	def exportTriangles(self, want_bounding_triangle=False): # Returns the triangles not including the bounding box stuff.
		if not want_bounding_triangle:

			return [(a-4, b-4, c-4) for (a,b,c) in self.triangles if a > 3 and b > 3 and c > 3]
		else:
			return self.triangles
	def exportVoronoi(self): # This returns the vertexes and the edges of the corresponding voronoi shit.
		useVertex = {i: [] for i in range(len(self.coords))} # This is the dictionary with the triangle index as a key and the value as the corresponding edges of that triangle. Construct this such that the key is always the last edge in the list.
		vor_coords = []
		index = {}
		# Build a list of coordinates and one index per triangle/region
		for tidx, (a,b,c) in enumerate(sorted(self.triangles)):
			vor_coords.append(self.circles[(a,b,c)][0]) # Get the first index, because the first index is the center point.
			# Insert triangle, rotating it so the key is the last vertex in the list.
			useVertex[a] += [(b,c,a)]
			useVertex[b] += [(c,a,b)]
			useVertex[c] += [(a,b,c)]
			# Set tidx as the index to use with this triangle.
			index[(a,b,c)] = tidx
			index[(b,c,a)] = tidx
			index[(c,a,b)] = tidx

		# init regions per coordinate dictionary.
		regions = {}
		# Sort each region in a coherent order, and substitute each triangle by its index.
		# for i in range(4, len(self.coords)): # Skip over the first triangles which is the bounding box stuff.
		for i in range(4, len(self.coords)):
			# The current vertex
			#if i not in useVertex or len(useVertex[i]) == 0:
			#	continue # This is just to shut up the warning.
			v = useVertex[i][0][0]
			r = []
			for _ in range(len(useVertex[i])): # Go over each 
				# Search the triangle from the very first vertex.
				t = [t for t in useVertex[i] if t[0] == v][0] # This get's the triangle vertex
				r.append(index[t])
				v = t[1] # Go to the next vertex
			regions[i-4] = r # Store the region into the set.
		return vor_coords, regions # Regions is the dict where the key is the index of the center point and the value is just the list of the associated 

	def render_polygon(self, polygon): # This renders the polygon.
		turtle.color("green")
		# First convert the polygon data structure to a list of points and then iterate over them.
		pts = []
		for (edge0, edge1, tri_op) in polygon:
			# Ok so the start edge is edge0 and the end edge is edge1
			p0 = self.coords[edge0]
			p1 = self.coords[edge1]
			p0,p1 = scale_points([p0,p1])
			turtle.penup()
			turtle.goto(p0)
			turtle.dot()
			turtle.pendown()
			turtle.goto(p1)
			turtle.dot()
			turtle.penup()
		turtle.update()
		#time.sleep(100)
		return




'''
Just a quick debug thing...

poopoofuck!!!!
p == [-0.06666667 -0.33333333]
Here is the current value of polygon: [(6, 12, (15, 12, 6)), (12, 14, (14, 12, 11)), (14, 16, (16, 14, 5)), (16, 0, (16, 10, 0)), (0, 17, (17, 0, 1)), (17, 13, (17, 1, 13)), (13, 6, (13, 8, 6))]
Here is the removed_shit: {(17, 6, 12), (17, 13, 6), (17, 12, 14), (17, 16, 0), (17, 14, 16)}


    for i, neigh in enumerate(self.triangles[tri_op]):
KeyError: (13, 8, 6)


'''
