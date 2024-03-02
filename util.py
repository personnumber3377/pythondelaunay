
import turtle

SCALE_FACTOR = 150


def scale_points(point_list: list) -> list: # This scales the points.
    out = []
    for p in point_list:
        assert len(p) == 2 # sanity checking
        p_x = p[0]
        p_y = p[1]
        out.append(tuple((p_x*SCALE_FACTOR, p_y*SCALE_FACTOR)))
    return out


def render_points(check_points, color="black"):
	turtle.speed(0)
	turtle.tracer(0,0)
	print("poopoofuck!!!!")
	#t = turtle.Turtle()
	#t.speed(10)
	turtle.color(color)
	turtle.penup()
	for p in check_points:
		turtle.goto((p[0]*SCALE_FACTOR, p[1]*SCALE_FACTOR))
		turtle.dot()
	turtle.update()
	return



def render_polygon(polygon, color="blue"):
    # t is the turtle
    # color is the... ya know... color
    '''
    t.penup()
    t.color(color)
    t.goto(polygon[0])
    t.pendown()
    for pos in polygon[1:]:
        t.goto(pos)
    t.goto(polygon[0])
    t.penup()
    '''
    polygon = scale_points(polygon)
    turtle.penup()
    turtle.color(color)
    turtle.goto(polygon[0])
    turtle.pendown()
    for pos in polygon[1:]:
        turtle.goto(pos)
    turtle.goto(polygon[0])
    turtle.penup()

    return


def check_multiple(lst): # This checks if there are duplicate elements in a list. Returns True if there are duplicates. False otherwsie
	set_shit = set(lst)
	return len(set_shit) != len(lst) # If the lengths are the same then there are NOT any duplicates.


def render_triangles(triangles: list, test_points: list, color="red") -> None: # This renders the triangles with turtle
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    turtle.color(color)
    turtle.speed(0)
    turtle.tracer(0,0)
    print("Called render_triangles")
    for tri in triangles:
        print("tri: "+str(tri))
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
        turtle.update()
    return



