
import turtle
import copy

def is_outside(point, radius):
    # This function checks if "point" is outside of the bounding box.
    x = point[0]
    y = point[1]
    if x > radius or x < -1*radius or y > radius or y < -1*radius:
        return True # The point is outside the bounding box.
    return False # Not outside the box.

def get_vec(prev_point, current_point): # Returns the vector from prev_point to current_point.
    return tuple((-1*prev_point[0]+current_point[0], -1*prev_point[1]+current_point[1]))



def ComputeIntersection(prev_point, current_point, clipEdge):
    # This computes the intersection between clipEdge and the vector created by the line from prev_point to cur_point.
    vec = get_vec(prev_point, current_point)
    #print("clipEdge == "+str(clipEdge))
    assert not (clipEdge[0] == None and clipEdge[1] == None)
    if clipEdge[1] == None: # The line is x = something
        print("Checking x shit")
        
        x_coord = clipEdge[0]
        # solve the equation prev_point[0] + k*vec[0] = x_coord => k = (x_coord - prev_point[0])/(vec[0])
        if vec[0] != 0:

            k =  (x_coord - prev_point[0])/(vec[0])
        else:
            k =  (x_coord - prev_point[0])
        # Now add vec*k to the previous point to get intersection point.
        intersec = tuple((prev_point[0]+k*vec[0], prev_point[1]+k*vec[1]))
        #print("intersec == "+str(intersec))
        return intersec
    else:
        print("Checking y shit")
        print("prev_point == "+str(prev_point))
        print("current_point == "+str(current_point))
        # The line is y = something
        # Just do the same, but with the y coordinate.
        print("clipEdge[1] == "+str(clipEdge[1]))
        y_coord = clipEdge[1]
        # solve the equation prev_point[0] + k*vec[0] = x_coord => k = (x_coord - prev_point[0])/(vec[0])
        if vec[1] != 0:

            k =  (y_coord - prev_point[1])/(vec[1])
        else:
            print("Special case!!!")
            k =  (y_coord - prev_point[1])
        # Now add vec*k to the previous point to get intersection point.
        intersec = tuple((prev_point[0]+k*vec[0], prev_point[1]+k*vec[1]))
        print("intersec == "+str(intersec))
        return intersec


def check_inside(point, edge): # Check if the point is inside the edge.
    point_x = point[0]
    point_y = point[1]
    assert not (edge[0] == None and edge[1] == None)
    if edge[1] == None: # Check for x coord.
        #print("Checking x coordinate!!!")
        x_coord = edge[0]
        if x_coord <= 0:
            return point_x >= x_coord
        else: # check for below.
            return point_x <= x_coord
    else:
        # Check for y coord.
        y_coord = edge[1]
        if y_coord <= 0:
            return point_y >= y_coord
        else: # check for below.
            return point_y <= y_coord
    # Should not happen.
    assert False


def sutherland_hodgman(points, radius):
    print("Called sutherland_hodgman")
    # This clips the polygon described by points against the box which is of distance "radius" from (0,0) . This assumes that the points list is in order (aka the points are in the order where you would connect them).
    '''
    List outputList = subjectPolygon;  

    for (Edge clipEdge in clipPolygon) do
        List inputList = outputList;
        outputList.clear();

        for (int i = 0; i < inputList.count; i += 1) do
            Point current_point = inputList[i];
            Point prev_point = inputList[(i − 1) % inputList.count];

            Point Intersecting_point = ComputeIntersection(prev_point, current_point, clipEdge)

            if (current_point inside clipEdge) then
                if (prev_point not inside clipEdge) then
                    outputList.add(Intersecting_point);
                end if
                outputList.add(current_point);

            else if (prev_point inside clipEdge) then
                outputList.add(Intersecting_point);
            end if

        done
    done
    '''

    out = points
    #for clipEdge in [(radius,None)]:
    #for clipEdge in [(radius,None),(-radius,None),(None, radius), (None, -radius)]: # This is just a list of the bounding box lines.
    #for clipEdge in [(None,radius)]:
    for clipEdge in [(radius,None),(-radius,None),(None, radius), (None, -radius)]:
        #inputList = copy.deepcopy(out) # This is bad for performance.
        inputList = out

        
        out = []
        for i in range(len(inputList)):
            current_point = inputList[i]
            prev_point = inputList[(i - 1) % len(inputList)]

            intersecting_point = ComputeIntersection(prev_point, current_point, clipEdge)
            print("intersecting_point == "+str(intersecting_point))
            if check_inside(current_point, clipEdge):
                if not check_inside(prev_point, clipEdge):
                    out.append(intersecting_point)
                out.append(current_point)
            elif check_inside(prev_point, clipEdge):
                out.append(intersecting_point)
    print("Length of the output list: "+str(len(out)))
    return out # Output the polygon.


def clip_polygon(points, radius): # This clips all of the points and shit.
    val_stuff = [is_outside(p, radius) for p in points]

    n_outside = sum(val_stuff)
    #assert n_outside < 2 # There should be no more than one point outside, because I don't know how to program the other cases. :D
    if n_outside == 0:
        print("n_outside == "+str(n_outside))
        # Just return the original point list, if all of the points are inside the box.
        return points
    print("Clipping!!!")
    # Now there should be the one point which is outside the stuff.
    # identify which point is outside.
    # Just implement this function: https://en.wikipedia.org/wiki/Sutherland%E2%80%93Hodgman_algorithm#Pseudocode
    poly = sutherland_hodgman(points, radius)

    return poly

def test_is_outside():
    radius = 10
    point = tuple((15,0))
    assert is_outside(point, radius)
    point = tuple((9.99,0))
    assert not is_outside(point, radius)
    # Edge case
    point = tuple((10.0,0.0))
    assert not is_outside(point, radius)
    print("test_is_outside passed!!!")
    return

def test_intersection():
    # def ComputeIntersection(prev_point, current_point, clipEdge):
    prev_point = (0,0)
    cur_point = (1,0)
    clipedge = (10,None)
    res = ComputeIntersection(prev_point, cur_point, clipedge)
    assert res == (10,0)
    print("test_intersection passed!!!")
    return

def test_inside_edge():
    point = (0,0)
    edge = (1,None)
    assert check_inside(point, edge)
    edge = (-1,None)
    assert check_inside(point, edge)
    point = (10,0)
    edge = (1,None)
    assert not check_inside(point, edge)
    print("test_inside_edge passed!")
    return

def run_tests():
    test_is_outside()
    test_intersection()
    test_inside_edge()
    return

SCALE_FACTOR = 5

def scale_points(point_list: list) -> list: # This scales the points.
    out = []
    for p in point_list:
        assert len(p) == 2 # sanity checking
        p_x = p[0]
        p_y = p[1]
        out.append(tuple((p_x*SCALE_FACTOR, p_y*SCALE_FACTOR)))
    return out


def render_polygon(polygon, t, color="blue"):
    # t is the turtle
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


def render_stuff(): # Renders some testcases.
    t = turtle.Turtle()
    t.speed(0)
    
    # Ok, so try clipping a polygon and then show the clipped stuff.
    radius = 30
    #original_points = [(0,10),(0,-10),(60,10)] # A long triangle
    #original_points = [(0,10),(0,-10),(60,55)] # A long triangle with one point which goes to the top right
    # original_points = [(0,10),(0,-10),(30,55)]
    original_points = [(0,0), (30,0), (30,50), (0,50)]
    render_polygon(scale_points(original_points), t)
    box_poly = [(-radius, -radius), (-radius, radius), (radius, radius), (radius, -radius)]
    render_polygon(scale_points(box_poly), t, color="purple")
    # Clip the polygon.
    clipped = clip_polygon(original_points, radius) # Clip.
    render_polygon(scale_points(clipped), t, color="red") # Show the clipped polygon in red

    return


def main(): # Just run the tests in the main function
    # radius = 40
    # [center+radius*np.array((-1, -1)), center+radius*np.array((+1, -1)), center+radius*np.array((+1, +1)), center+radius*np.array((-1, +1))]
    run_tests()
    while True: # Run only once.
        render_stuff()

if __name__=="__main__":
    exit(main())
