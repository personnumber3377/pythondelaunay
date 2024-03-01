
# This is an implementation of Lloyd's algorithm with the Delaunay triangulation Voronoi diagram.  https://en.wikipedia.org/wiki/Lloyd%27s_algorithm

from delaunay import * # Import the Delaunay stuff
import turtle
import math
from triangle_clipping import * # this is for clip_polygon(original_points, radius)
from check_inside import *
import random

MOVE_SPEED = 2
SCALE_FACTOR = 5
import time


def gen_random_color(): # Generates a random color as a string: "#rrggbb" hex .
    # col = "#"+''.join([hex(random.randrange(0,256))[2:] for _ in range(3)]) # This doesn't work, because hex(10) = "0xa" . We expect the hex shit to be two characters long after the "0x" prefix.
    
    # Thanks to https://stackoverflow.com/questions/12638408/decorating-hex-function-to-pad-zeros
    # "{:02x}".format(7)
    
    col = "#"+''.join(["{:02x}".format(random.randrange(0,256)) for _ in range(3)])
    assert len(col) == len("#b01e91")
    return col

def render_points(t, check_points, color="black"):
    t.color(color)
    t.penup()
    for p in check_points:
        t.goto((p[0]*SCALE_FACTOR, p[1]*SCALE_FACTOR))
        t.dot()
    return



def gen_points(min_x, max_x, min_y, max_y, step_size): # This generates a box of points
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
    return check_points




def render_triangles(triangles: list, test_points: list) -> None: # This renders the triangles with turtle
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
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



def shift_list(lst, start_index):
    # Shifts a list.
    point_index_bullshit = lst
    
    # Now cut the list at start_index.
    point_index_bullshit_copy = copy.deepcopy(point_index_bullshit)
    search_shit = point_index_bullshit_copy[start_index:]

    other_shit = point_index_bullshit_copy[:start_index]

    search_shit = search_shit + other_shit

    assert search_shit[start_index] == point_index_bullshit[0]

    return search_shit

def get_weight_color(weight, weights): # This returns a shade of blue. The darker it is, the more weight.
    
    #col = "#"+''.join(["{:02x}".format(random.randrange(0,256)) for _ in range(3)])
    #assert len(col) == len("#b01e91")
    # rgb
    print("fuck")
    base = "#0000"
    max_weight = max(weights)
    if max_weight == 0:
        max_weight = 1
    blue = "{:02x}".format(round(weight/max_weight*255)) # Just the proportional thing.
    print("blue == "+str(blue))
    assert len(blue) == 2
    
    return base+blue



def render_polygon(polygon, t, color="blue"):
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

    turtle.penup()
    turtle.color(color)
    turtle.goto(polygon[0])
    turtle.pendown()
    for pos in polygon[1:]:
        turtle.goto(pos)
    turtle.goto(polygon[0])
    turtle.penup()

    return


def scale_points(point_list: list) -> list: # This scales the points.
    out = []
    for p in point_list:
        assert len(p) == 2 # sanity checking
        p_x = p[0]
        p_y = p[1]
        out.append(tuple((p_x*SCALE_FACTOR, p_y*SCALE_FACTOR)))
    return out

def scale_point(point): # This scales just one point
    return tuple((point[0]*SCALE_FACTOR, point[1]*SCALE_FACTOR))

class Lloyd:
    def __init__(self, points: list, center=(0,0), radius=1000):
        self.points = points
        self.center = center
        self.radius = radius
        self.delaunay_diagram = Delaunay(center=center, radius=radius)
        for p in self.points:
            self.delaunay_diagram.addPoint(p)
        self.circumcenters, self.regions = self.delaunay_diagram.exportVoronoi()
    def updateDelaunay(self) -> None: # This assumes that self.points has been reassigned.
        self.delaunay_diagram = Delaunay(center=self.center, radius=self.radius)
        for p in self.points:
            self.delaunay_diagram.addPoint(p)
    def updateVoronoi(self) -> None: # This assumes that updateDelaunay has been called
        self.circumcenters, self.regions = self.delaunay_diagram.exportVoronoi()

    def update(self): # Set's the points to the current centroids of the regions.
        print("New cycle!!!")
        new_points = [] # This will be assigned to self.points later on.
        polygons = self.regions
        cells = polygons
        # Get the current centroids and assign the points to them.
        #cur_centroids = [self.get_centroid(poly) for poly in polygons] # These are the current centroids.
        cur_centroids = [self.get_centroid(self.regions[poly]) for poly in polygons] # These are the current centroids.
        self.prev_centroids = cur_centroids
        # Lerp the points forward a bit.
        print("Length of cur_centroids: "+str(len(cur_centroids)))
        print("Length of the centroids: "+str(len(cur_centroids)))
        # Show the current centroids.
        #self.draw_points(points=cur_centroids) # Just draw the centroids.
        
        for i in range(len(self.points)):
            p = self.points[i]
            centroid = cur_centroids[i]
            # Add a bit of the centroid vector to the point.
            p_to_centroid_vec = (-p[0]+centroid[0], -p[1]+centroid[1])
            how_much_to_advance = (p_to_centroid_vec[0]*MOVE_SPEED, p_to_centroid_vec[1]*MOVE_SPEED)
            new_points.append((p[0]+how_much_to_advance[0], p[1]+how_much_to_advance[1])) # Add the vector.
            # Sanity check.
            #assert math.sqrt((new_points[-1][0]**2)+(new_points[-1][1]**2)) <= self.radius
        # Instead of an assert, let's put a thing which just forces the point to be inside the stuff.

        # assign the moved points to self.points
        self.points = new_points
        self.check_points() # Bounds check.
        # Sanity check.
        #assert all(math.sqrt((p[0]**2)+(p[1]**2)) <= self.radius for p in self.points)
        # Now just update the delaunay and voronoi stuff.
        self.updateDelaunay()
        self.updateVoronoi()


    def render_voronoi_debug(self, t):
        turtle.tracer(0,0)
        turtle.speed(0)
        for i, poly in enumerate(self.regions):
            #turtle.clearscreen()
            polygon_points_indexes = self.regions[poly]
            # pts = [self.circumcenters[point_indexes[i]] for i in range(len(point_indexes))]
            points = [self.circumcenters[polygon_points_indexes[j]] for j in range(len(polygon_points_indexes))]
            # render_polygon(scale_points(points), t, color="red")
            print("points == "+str(points))
            render_polygon(scale_points(points), turtle, color=get_weight_color(self.weights[i], self.weights)) # The color signifies the weights.

            print("self.weights == "+str(self.weights))
            #t.update()
            #turtle.clear()
            turtle.update()
            #turtle.clear()
            #input("Press any key to continue..-")
            #turtle.clearscreen()
            #turtle.clearscreen()
            #turtle.clear()
        time.sleep(2)
        turtle.clear()
        return



    def get_polygon_index(self, point, start_index=0): # Get's the index in the current polygons, where the point is inside of .
        # Get's the index of the polygon in self.polygons which contains inside the point called "point"

        point_index_bullshit = [self.regions[poly] for poly in self.regions]
        #print("point_index_bullshit[0] == "+str(point_index_bullshit[0]))
        # Now cut the list at start_index.
        point_index_bullshit_copy = copy.deepcopy(point_index_bullshit)
        search_shit = point_index_bullshit_copy[start_index:]

        other_shit = point_index_bullshit_copy[:start_index]

        search_shit = search_shit + other_shit
        #print("search_shit[start_index] == "+str(search_shit[start_index]))
        assert len(search_shit) == len(point_index_bullshit) # Sanity.
        assert search_shit[0] == point_index_bullshit[start_index]

        on_first_try = False
        for i, polygon_points_indexes in enumerate(search_shit):
            #polygon_points_indexes = self.regions[poly]
            # pts = [self.circumcenters[point_indexes[i]] for i in range(len(point_indexes))]
            points = [self.circumcenters[polygon_points_indexes[j]] for j in range(len(polygon_points_indexes))]

            #print("points == "+str(points))

            #print("Here is the points inside get_polygon_index: "+str(points))
            # Now check if the point is inside the polygon drawn out by connecting every point in the "points" list.
            # def check_inside_poly(point, polygon):
            res = check_inside_poly(point, points)
            if res:
                # Is inside so return the current index.
                #print("Returning actual: "+str(i))

                #return i
                # Instead of returning i, we need to return the index into the original index, so do some modulo magic.
                return (start_index + i) % len(search_shit), on_first_try
            on_first_try = False
        # The point is not inside of any polygon
        #assert False
        #return 0 # Just shut up.
        # Now just return the last index.
        return start_index, False

        #print("Returning oof")
        return "oof"

    def debug_polygon_shit(self): # This should show us the points which do not get assigned to any polygon.
        # First create a box of points.
        # def gen_points(min_x, max_x, min_y, max_y, step_size):

        points = gen_points(-self.radius, self.radius, -self.radius, self.radius, 0.5) # Box of points.
        t = turtle.Turtle()
        turtle.tracer(0,0)
        turtle.speed(0)

        # First render the polygons.

        self.render_voronoi_debug(t)
        turtle.update()
        input()
        #render_points(t, points) # First show all of them 
        # self.get_polygon_index(point)
        # if that function returns "oof" , then we know that that said point is not assigned to any voronoi polygon.
        unassigned_points = []
        cur_index = None
        index_shit = [[] for _ in range(len(self.regions)+1)] # +1 for the unassigned area
        #cur_polygon_shit = []
        last_found_index = 0
        for p in points:
            # Check for new index
            index, _ = self.get_polygon_index(p, start_index=last_found_index)
            last_found_index = index
            #if index == "oof":
            #    index = len(index_shit)-1 # Just get the last index
                # actually just skip this.
                #continue
            index_shit[index].append(p)

            #if self.get_polygon_index(p) !=:
            #    unassigned_points.append(p)
        #assert len(index_shit[-1]) == 0
        print("sum([len(x) for x in index_shit]) == "+str(sum([len(x) for x in index_shit])))
        print("len(points) == "+str(len(points)))
        assert sum([len(x) for x in index_shit]) == len(points)
        print("length of the index_shit: "+str(len(index_shit)-1))
        for indexes in index_shit:
            # indexes is a list of points, all of which are inside the exact same polygon. First generate a random color and then show the points.
            ran_color = gen_random_color()
            render_points(t, indexes, color=ran_color)
            turtle.update()
            input()

        # Just render the other shit too.
        #self.render()
        turtle.update()
        time.sleep(50)
        return

    def update_weighted(self, image_data): # Image data is the pixel data of the image.
        # See https://editor.p5js.org/codingtrain/sketches/Z_YV25_4G
        #self.debug_polygon_shit()
        print("New cycle!!!")
        new_points = [] # This will be assigned to self.points later on.
        print("self.regions == "+str(self.regions))
        polygons = self.regions
        cells = polygons
        r = self.radius
        # Get the current centroids and assign the points to them.
        #cur_centroids = [self.get_centroid(poly) for poly in polygons] # These are the current centroids.


        #cur_centroids = [self.get_centroid(self.regions[poly]) for poly in polygons] # These are the current centroids.

        #self.prev_centroids = cur_centroids
        
        
        # Before lerping, we need to calculate the weights of each thing.
        '''
        for i in range(len(image_data)):
            for j in range(len(image_data[0])):
                # Get the brightness
                brightness = (pix[0]+pix[1]+pix[2])/3.0
                w = 1 - (brightness/255)
                centroid_index = self.get_index()
        '''

        centroids = [[0,0] for _ in range(len(polygons))] # Initialize to (0,0)
        weights = [0.0 for _ in range(len(centroids))] # All of the weights
        self.weights = weights
        # Ok, so image_data is the points and the brightnesses.
        tot_count = 0
        complete_count = len(image_data)*len(image_data[0])

        point_count = 6000 # Generate six thousand points.
        
        # Do not modify this shit here. it will break shit.
        cur_start_index = 0
        first_try_count = 1
        tot_count = 1
        #print("initial centroids: "+str(centroids))
        for i in range(len(image_data)):
            #print(str(tot_count/complete_count*100)+" percent done")
            #print("First try count: "+str(first_try_count/(tot_count)*100))
            for j in range(len(image_data[0])):
                pix = image_data[i][j]
                print("pix == "+str(pix))
                print("pix[0] == "+str(pix[0]))
                print("pix[1] == "+str(pix[1]))
                print("pix[2] == "+str(pix[2]))
                pix = [float(x) for x in pix]
                point = ((i/(len(image_data)))*r*2-(r), j/(len(image_data[0]))*r*2-(r))
                brightness = (pix[0]+pix[1]+pix[2])/3.0
                print("pix[0]+pix[1]+pix[2] == "+str(pix[0]+pix[1]+pix[2]))
                print("Brightness: "+str(brightness))
                weight = 1 - (brightness / 255)
                
                cor_index, first_try = self.get_polygon_index(point, start_index=cur_start_index)
                #print("cor_index == "+str(cor_index))
                #print("cur_start_index == "+str(cur_start_index))
                first_try_count += int(first_try)
                tot_count += 1
                cur_start_index = cor_index

                #print("cor_index == "+str(cor_index))
                # Now update the weight shit of the centroids using the correct index. Just follow this: https://editor.p5js.org/codingtrain/sketches/Z_YV25_4G
                #centroids[cor_index][0] += i*weight
                #centroids[cor_index][1] += j*weight
                #print("centroids[cor_index] == "+str(centroids[cor_index]))


                centroids[cor_index][0] += (point[0])*weight
                centroids[cor_index][1] += (point[1])*weight
                weights[cor_index] += weight # Add the weight to the weights

                tot_count += 1 # Add one to the counter.

        print("Calculated the weight shit..")
        # Now divide the centroids by the weights
        for i in range(len(centroids)):
            if weights[i] > 0: # avoid division by zero.
                centroids[i] = (centroids[i][0]/weights[i], centroids[i][1]/weights[i])
            else:
                centroids[i] = self.points[i] # Just copy.

        centroids = [list(x) for x in centroids]

        cur_centroids = centroids
        self.prev_centroids = centroids
        # Lerp the points forward a bit.
        print("Length of cur_centroids: "+str(len(cur_centroids)))
        print("Length of the centroids: "+str(len(cur_centroids)))
        # Show the current centroids.
        #self.draw_points(points=cur_centroids) # Just draw the centroids.
        
        #for i in range(len(self.points)):
        for i in range(len(cur_centroids)):
            p = self.points[i]
            centroid = cur_centroids[i]
            # Add a bit of the centroid vector to the point.
            p_to_centroid_vec = (-p[0]+centroid[0], -p[1]+centroid[1])
            how_much_to_advance = (p_to_centroid_vec[0]*MOVE_SPEED, p_to_centroid_vec[1]*MOVE_SPEED)
            new_points.append((p[0]+how_much_to_advance[0], p[1]+how_much_to_advance[1])) # Add the vector.
            # Sanity check.
            #assert math.sqrt((new_points[-1][0]**2)+(new_points[-1][1]**2)) <= self.radius
        # Instead of an assert, let's put a thing which just forces the point to be inside the stuff.

        # assign the moved points to self.points
        self.points = new_points
        self.check_points() # Bounds check.
        # Sanity check.
        #assert all(math.sqrt((p[0]**2)+(p[1]**2)) <= self.radius for p in self.points)
        # Now just update the delaunay and voronoi stuff.
        self.updateDelaunay()
        self.updateVoronoi()


    def check_points(self):
        point_list = self.points
        # Go over each point and do the bounds check.
        dist_bound = self.radius
        clipped = False
        for i, p in enumerate(point_list):
            point_list[i] = list(point_list[i])
            if p[0] > dist_bound:
                clipped = True
                point_list[i][0] = dist_bound
            elif p[0] < -1*dist_bound:
                point_list[i][0] = -1*dist_bound
                clipped = True
            if p[1] > dist_bound:
                point_list[i][1] = dist_bound
                clipped = True
            elif p[1] < -1*dist_bound:
                point_list[i][1] = -1*dist_bound
                clipped = True

            assert math.sqrt((point_list[i][0]**2)+(point_list[i][1]**2)) <= self.radius*2

            point_list[i] = tuple(point_list[i])
        if clipped:
            print("We have clipped some points!!!")
        self.points = point_list
        return

    def get_centroid(self, region) -> tuple: # This computes the rough centroid. (Using the average of all of the points in the region)
        # Ok so this assumes that the region is the value in the self.regions dictionary, so the region is a list of point indexes.
        point_indexes = region
        pts = [self.circumcenters[point_indexes[i]] for i in range(len(point_indexes))]
        # pts is the stuff which enscribes one of the regions.
        #pts = self.check_clipping(pts)
        # self.circumcenters, self.regions

        # Now at this point check for clipping using triangle_clipping.py: 
        new_points = clip_polygon(copy.deepcopy(pts), self.radius)

        # Draw the clipped shit.
        # def render_polygon(polygon, t, color="blue"):
        t = turtle.Turtle()
        t.speed(0)
        turtle.tracer(0, 0)
        render_polygon(scale_points(new_points), t, color="green")
        turtle.update()
        #time.sleep(0.05) # Sleep to show the green stuff
        # Now calculate rough centroid. Clip first
        #return (sum([p[0] for p in pts])/len(pts), sum([p[1] for p in pts])/len(pts)) # Return the average of the coordinates. This is not the actual centroid, but close enough.
        # new_points
        #return (sum([p[0] for p in new_points])/len(new_points), sum([p[1] for p in new_points])/len(new_points))

        # Ok, so at this point I have the clipped triangle in new_points. Let's apply the appropriate equations to it to get the centroid.

        '''
        for (let poly of cells) {
    let area = 0;
    let centroid = createVector(0, 0);
    for (let i = 0; i < poly.length; i++) {
      let v0 = poly[i];
      let v1 = poly[(i + 1) % poly.length];
      let crossValue = v0[0] * v1[1] - v1[0] * v0[1];
      area += crossValue;
      centroid.x += (v0[0] + v1[0]) * crossValue;
      centroid.y += (v0[1] + v1[1]) * crossValue;
    }
    area /= 2;
    centroid.div(6 * area);
    centroids.push(centroid);
  }
        '''

        area = 0
        centroid = [0,0] # Convert to tuples later on.
        for i in range(len(new_points)):
            # (assumes that the points are in order.)
            v0 = new_points[i]
            v1 = new_points[(i + 1) % len(new_points)]
            crossValue = v0[0] * v1[1] - v1[0] * v0[1]
            area += crossValue
            centroid[0] += (v0[0] + v1[0]) * crossValue
            centroid[1] += (v0[1] + v1[1]) * crossValue
        area /= 2
        centroid = (centroid[0]/(6*area), centroid[1]/(6*area))
        return centroid

    def check_clipping(self, points: list): # This makes it such that none of the points are outside of the bounding box.
        dist_bound = self.radius
        for i, p in enumerate(points):
            # Ripped straight from check_points.
            p = list(p)
            points[i] = list(points[i])
            if p[0] > dist_bound:
                clipped = True
                points[i][0] = dist_bound
            elif p[0] < -1*dist_bound:
                points[i][0] = -1*dist_bound
                clipped = True
            if p[1] > dist_bound:
                points[i][1] = dist_bound
                clipped = True
            elif p[1] < -1*dist_bound:
                points[i][1] = -1*dist_bound
                clipped = True
            points[i] = tuple(points[i])
            print("points[i] == "+str(points[i]))
        return points

    def render(self) -> None: # Renders the stuff.
        turtle.speed(0)
        turtle.tracer(0, 0)
        voronoi_regions = self.regions
        voronoi_points = self.circumcenters
        #def render_voronoi(voronoi_points: list, voronoi_regions: dict) -> None: # This is taken straight from main.py
        # Render all of the regions.
        t = turtle.Turtle()
        print("voronoi_regions == "+str(voronoi_regions))
        '''
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
            t.goto(scale_points([voronoi_points[point_indexes[0]]])[0])
            t.penup()
        '''
        t.penup()
        # Draw bounding box.
        self.draw_bounding(t)
        self.draw_bounding_triangle(t)
        self.draw_points(t=t)
        self.draw_points(t=t, points=self.prev_centroids)
        turtle.update()
        #time.sleep(0.01)
    def draw_bounding(self, t):
        t.color("blue")
        r = self.radius*SCALE_FACTOR # Just assign a constant
        points = [(-1*r, 1*r), (r,r), (r,-1*r), (-1*r, -1*r), (-1*r, 1*r)]
        t.penup()
        t.goto(points[0])
        t.pendown()
        for p in points[1:]:
            t.goto(p)
        t.penup()
        return

    def draw_bounding_triangle(self, t):
        # The vertexes are at these coordinates: [center+radius*np.array((-1, -1)), center+radius*np.array((+1, -1)), center+radius*np.array((+1, +1)), center+radius*np.array((-1, +1))]
        radius = self.radius
        center = np.asarray(self.center)
        tri_points = [center+radius*np.array((-1, -1)), center+radius*np.array((+1, -1)), center+radius*np.array((+1, +1)), center+radius*np.array((-1, +1))]
        tri_points = scale_points(tri_points)
        t.color("purple")
        t.penup()
        t.goto(tri_points[0])
        t.pendown()
        for p in tri_points:
            t.goto(p)
        t.goto(tri_points[0])
        t.penup()
        return
    
    def draw_points(self, t=None, points=None): # This draws all of the points.
        
        if t == None:
            t = turtle.Turtle()
        turtle.speed(0)
        t.penup()
        if points == None:
            points = self.points
        t.color("black")
        for p in points:
            # Just place a dot everywhere where the points are.
            t.goto(scale_point(p))
            t.dot()
        turtle.update()
        return

    def render_delaunay(self):
        # tris = delaunay.exportTriangles()
        tris = self.delaunay_diagram.exportTriangles()


        render_triangles(tris, self.points)
        turtle.update()


def main() -> int:
    # First generate testdata:
    numSeeds = 100
    radius = 40
    seeds = radius * np.random.random((numSeeds, 2))
    #seeds = [(10,0),(-10,0),(0,-10),(0,10),(10,10)]
    #seeds = [(x*5,x) for x in range(-5,5,1)]
    #seeds = [(-10,0), (10,0), (10,10)]
    #seeds = [(-10,0), (10,0), (0,10)]
    # First declare the Lloyd object.
    #lloyd = Lloyd(seeds)
    lloyd = Lloyd(seeds, center=(0,0), radius=50)
    # We basically wan't to move the points until the points are are at the centroids of the voronoi cells.
    while True:
        # First update, then render.
        lloyd.update()
        #lloyd.update_weighted()
        turtle.clearscreen()
        lloyd.render()
        lloyd.render_delaunay() # tris = delaunay.exportTriangles()
        #time.sleep(0.1)
    return 0

if __name__=="__main__": # Runs tests.
    exit(main())

