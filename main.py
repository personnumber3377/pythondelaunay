
# This is a driver file for the delaunay file.
from delaunay import *
import turtle

SCALE_FACTOR = 30

def scale_points(point_list: list) -> list: # This scales the points.
	out = []
	for p in point_list:
		p_x = p[0]
		p_y = p[1]
		out.append(tuple((p_x*SCALE_FACTOR, p_y*SCALE_FACTOR)))
	return out

def render_triangles(triangles: list, test_points: list) -> None: # This renders the triangles with turtle
	t = turtle.Turtle()
	t.speed(0)
	t.penup()
	for tri in triangles:
		#print("tri: "+str(tri))
		# OK, so tri is a list of the indexes to the points list, therefore get points.
		p1 = test_points[tri[0]]
		p2 = test_points[tri[1]]
		p3 = test_points[tri[2]]

		triangle_points = scale_points([p1,p2,p3])
		turtle.goto(triangle_points[0])
		turtle.pendown()
		turtle.goto(triangle_points[1])
		turtle.goto(triangle_points[2])
		turtle.goto(triangle_points[0])
		turtle.penup()
		turtle.update
	return

def render_voronoi(voronoi_points: list, voronoi_regions: dict) -> None:
	# Render all of the regions.
	t = turtle.Turtle()
	print("voronoi_regions == "+str(voronoi_regions))
	t.color("red")
	for reg in voronoi_regions:
		point_indexes = voronoi_regions[reg]
		t.penup()
		t.goto(scale_points([voronoi_points[point_indexes[0]]])[0])
		t.pendown()
		for p in point_indexes:
			print("p == "+str(p))
			#t.pendown()
			print("voronoi_points[p] == "+str(voronoi_points[p]))
			t.goto(scale_points([voronoi_points[p]])[0])
			
		t.penup()


def main() -> int:
	# def __init__(self, center=(0,0), radius=1000):
	numSeeds = 24
	radius = 10
	seeds = radius * np.random.random((numSeeds, 2))
	delaunay = Delaunay(radius=20)
	# Test points.
	#test_points = [(0,0),(0,5),(5,0),(1, 2)] # Should create a simple triangle
	test_points = seeds
	
	for p in test_points:
		delaunay.addPoint(p)
	tris = delaunay.exportTriangles()
	voronoi_points, voronoi_regions = delaunay.exportVoronoi()
	print("voronoi_regions == "+str(voronoi_regions))
	print("voronoi_points == "+str(voronoi_points))
	#assert all([len(x) == 3 for x in voronoi_regions])
	while True:
		render_triangles(tris, test_points)
		render_voronoi(voronoi_points, voronoi_regions)
	return 0

if __name__=="__main__":
	exit(main())


