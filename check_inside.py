







import turtle
import copy
import time

SCALE_FACTOR = 60

def render_points(t, check_points, color="black"):
    t.color(color)
    t.penup()
    for p in check_points:
        t.goto((p[0]*SCALE_FACTOR, p[1]*SCALE_FACTOR))
        t.dot()

def check_intersection_quick(p0, p1, y_coord):
    y0 = p0[1]
    y1 = p1[1]
    # If both points are on the other side of the y = something line, then of course they can't intersect.
    if (y0 <= y_coord and y1 <= y_coord) or (y0 >= y_coord and y1 >= y_coord):
        # No intersection
        return False
    return True

def handle_vertical(p0, p1, point):
    y_range = [p0[1], p1[1]] # This is the y range to check against.
    min_y_coord = point[1]
    y_range = [min(y_range), max(y_range)]
    assert y_range[0] <= y_range[1]
    y_coord = point[1]
    if y_coord >= y_range[0] and y_coord <= y_range[1]:
        #return True
        #print("y_coord == "+str(y_coord))
        #print("min_y_coord == "+str(min_y_coord))
        return point[0] >= p0[0]
    return False


def handle_horizontal(p0, p1, point):
    return False # Impossible, because we are only considering casting a horizontal ray. A horizontal ray can not intersect another horizontal line.
    min_x_coord = point[0]
    x_range = [p0[0], p1[0]] # This is the y range to check against.
    x_range = [min(x_range), max(x_range)]
    assert x_range[0] <= x_range[1]
    x_coord = point[0]
    if x_coord >= x_range[0] and x_coord <= x_range[1]:
        return x_coord >= min_x_coord
    return False



def check_intersection_complex(p0, p1, point): # The point is used here to check for the intersections which are greater than it.
    min_x_coord = point[0]
    y_coord = point[1]
    # First convert the formula to the y - y1 = m * (x - x1)   m = (y1-y0)/(x1-x0)
    # => x = (m * x1 + y - y1)/m
    #print("p0 == "+str(p0))
    #print("p1 == "+str(p1))
    x0 = p0[0]
    y0 = p0[1]
    x1 = p1[0]
    y1 = p1[1]
    if (x1 - x0) == 0:
        #print("now handling vertical line")
        # The points have the same x coordinate, therefore the line is a vertical line. (in the xy-plane).
        res = handle_vertical(p0, p1, point)
        #print("res == "+str(res))
        #return res
        return res
        #return False
    m = (y1 - y0)/(x1 - x0)
    if m == 0.0: # Division by zero.
        return handle_horizontal(p0, p1, point)
        #return False
    x_value = (m * x1 + y_coord - y1)/m
    if x_value > min_x_coord: # Always just go to the right.
        return True
    else:
        return False


def render_polygon(polygon, t, color="blue"):
    # t is the turtle
    polygon = scale_points(polygon)
    # color is the... ya know... color
    t.penup()
    t.color(color)
    t.goto(polygon[0])
    t.pendown()
    for pos in polygon[1:]:
        t.goto(pos)
    t.goto(polygon[0])
    t.penup()
    return

def scale_points(point_list: list) -> list: # This scales the points.
    out = []
    for p in point_list:
        assert len(p) == 2 # sanity checking
        p_x = p[0]
        p_y = p[1]
        out.append(tuple((p_x*SCALE_FACTOR, p_y*SCALE_FACTOR)))
    return out



def check_inside_poly(point, polygon):
    # Go over each side.
    y_coord = point[1] # I am just going to use the line y = something to check, because I am lazy
    copy_polygon = copy.deepcopy(polygon)
    copy_polygon.append(copy.deepcopy(copy_polygon[0])) # This simplifies the code a bit.
    count = 0
    for i in range(len(copy_polygon) - 1):
        prev_point = copy_polygon[i]
        cur_point = copy_polygon[i+1]
        # Now check for the intersection.
        if check_intersection_quick(prev_point, cur_point, y_coord):
            # Now check for a more complex intersection.
            #print("Poopoo")
            if check_intersection_complex(prev_point, cur_point, point):
                # Inside 
                count += 1
    #print("Count: "+str(count))
    return bool(count % 2)

def run_inside_test(): # A simple test which shows the points which are inside and which are outside of a certain polygon.
    #example_polygon = [(-1,-1), (-1,1), (1,1), (1,-1)] # A simple box.
    example_polygon = [(-2,0), (2,0), (0,2)]
    min_x = -3
    max_x = 3
    min_y = -3
    max_y = 3
    step_size = 0.1 # How far away are the evenly put points.
    
    check_points = []
    x = min_x
    y = min_y
    while y <= max_y:
        x = min_x
        while x <= max_x:
            point = (x,y)
            check_points.append(point)
            x += step_size
        y += step_size
    #check_points = [(0,0)] # Just a debug point.
    # Now we have a grid of points in check_points.
    # Render all of them first
    #while True:
    t = turtle.Turtle()
    turtle.tracer(0,0)
    turtle.speed(0)
    render_points(t, check_points) # First show all of them 

    # Show the bounding polygon:

    render_polygon(example_polygon, t, color="blue")

    turtle.update()
    # Now calculate the points which are inside the polygon.
    red_points = []
    for p in check_points:
        if check_inside_poly(p, example_polygon): # check if inside
            # add to list
            red_points.append(p)
    render_points(t, red_points, color="red")
    turtle.update()
    time.sleep(3)
    return


def run_tests():
    run_inside_test()

def main():
    run_tests()
    return 0

if __name__=="__main__":
    exit(main())
