
# This is an implementation of Lloyd's algorithm with the Delaunay triangulation Voronoi diagram.  https://en.wikipedia.org/wiki/Lloyd%27s_algorithm

from delaunay import * # Import the Delaunay stuff
import turtle
import math

MOVE_SPEED = 0.1
SCALE_FACTOR = 5
import time

def scale_points(point_list: list) -> list: # This scales the points.
    out = []
    for p in point_list:
        assert len(p) == 2 # sanity checking
        p_x = p[0]
        p_y = p[1]
        out.append(tuple((p_x*SCALE_FACTOR, p_y*SCALE_FACTOR)))
    return out



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
        new_points = [] # This will be assigned to self.points later on.
        polygons = self.regions
        cells = polygons
        # Get the current centroids and assign the points to them.
        #cur_centroids = [self.get_centroid(poly) for poly in polygons] # These are the current centroids.
        cur_centroids = [self.get_centroid(self.regions[poly]) for poly in polygons] # These are the current centroids.
        # Lerp the points forward a bit.
        print("Length of cur_centroids: "+str(len(cur_centroids)))
        print("Length of the centroids: "+str(len(cur_centroids)))
        for i in range(len(self.points)):
            p = self.points[i]
            centroid = cur_centroids[i]
            # Add a bit of the centroid vector to the point.
            p_to_centroid_vec = (-p[0]+centroid[0], -p[1]+centroid[1])
            how_much_to_advance = (p_to_centroid_vec[0]*MOVE_SPEED, p_to_centroid_vec[1]*MOVE_SPEED)
            new_points.append((p[0]+how_much_to_advance[0], p[1]+how_much_to_advance[1])) # Add the vector.
            # Sanity check.
            assert math.sqrt((new_points[-1][0]**2)+(new_points[-1][1]**2)) <= self.radius
        # assign the moved points to self.points
        self.points = new_points
        # Now just update the delaunay and voronoi stuff.
        self.updateDelaunay()
        self.updateVoronoi()

    def get_centroid(self, region) -> tuple: # This computes the rough centroid. (Using the average of all of the points in the region)
        # Ok so this assumes that the region is the value in the self.regions dictionary, so the region is a list of point indexes.
        point_indexes = region
        pts = [self.circumcenters[point_indexes[i]] for i in range(len(point_indexes))]
        # pts is the stuff which enscribes one of the regions.
        # Now calculate rough centroid.
        return (sum([p[0] for p in pts])/len(pts), sum([p[1] for p in pts])/len(pts)) # Return the average of the coordinates. This is not the actual centroid, but close enough.
    
    def render(self) -> None: # Renders the stuff.
        turtle.speed(0)
        turtle.tracer(0, 0)
        voronoi_regions = self.regions
        voronoi_points = self.circumcenters
        #def render_voronoi(voronoi_points: list, voronoi_regions: dict) -> None: # This is taken straight from main.py
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
        turtle.update()
        time.sleep(0.2)




def main() -> int:
    # First generate testdata:
    numSeeds = 50
    radius = 3
    seeds = radius * np.random.random((numSeeds, 2))
    # First declare the Lloyd object.
    #lloyd = Lloyd(seeds)
    lloyd = Lloyd(seeds, center=(0,0), radius=50)
    # We basically wan't to move the points until the points are are at the centroids of the voronoi cells.
    while True:
        # First update, then render.
        lloyd.update()
        lloyd.render()
        turtle.clearscreen()
    return 0

if __name__=="__main__": # Runs tests.
    exit(main())

