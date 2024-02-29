
import sys
from lloyd import *
from image_helper import *

def main(): # Loads an image called image.png and then shows the voronoi stippling of that image.
    if len(sys.argv) == 1: # One argument only.
        image_file = "image.png"
    else:
        image_file = sys.argv[-1] # Get the last file.
    print("Loading file: "+str(image_file))
    img = load_image(image_file)

    r = 50


    # Now create the points for areas which are dark.
    pts = []
    all_points = []
    for i in range(len(img)):
        cur_line = []
        for j in range(len(img[0])):
            # The current pixel is img[i][j] and should be a flat list of length three (or maybe four)???
            pix = img[i][j]
            assert len(pix) == 4 or len(pix) == 2
            #print("Here is the pixel: "+str(pix))
            # Get brightness
            #print("pix[0] == "+str(pix[0]))
            #print("pix[1] == "+str(pix[1]))
            #print("pix[2] == "+str(pix[2]))

            #assert all(isinstance(x, float) for x in pix)
            
            temp = sum(float(x) for x in pix[:3])
            brightness = (temp)/3.0
            assert isinstance(brightness, float)
            assert brightness >= 0 and brightness <= 255
            if brightness < 100: # We want DARK spots, not light spots. Therefore less than.
                actual_point = (((i/(len(img)))*r*2-(r), j/(len(img[0]))*r*2-(r)), brightness) # How far along the x coordinates we are times the radius giving us the correct place.
                # Sanity checks.
                # The point should not be outside of the bounding box.

                x = actual_point[0][0]
                y = actual_point[0][1]
                #print("x == "+str(x))
                #print("y == "+str(y))
                assert x >= -1*r and x <= r and y >= -1*r and y <= r # Sanity
                #print("Point passed!!!")
                cur_line.append(actual_point)
                all_points.append(actual_point[0])
        pts.append(cur_line)
    print("Processed image")
    # Ok, so I have every pixel, which is dark enough in the pts list. it is time to update the stuff.
    # Now finally do the stuff

    # First generate testdata:
    numSeeds = 30
    radius = 40
    seeds = radius * np.random.random((numSeeds, 2))
    #seeds = [(10,0),(-10,0),(0,-10),(0,10),(10,10)]
    #seeds = [(x*5,x) for x in range(-5,5,1)]
    #seeds = [(-10,0), (10,0), (10,10)]
    #seeds = [(-10,0), (10,0), (0,10)]
    # First declare the Lloyd object.
    #lloyd = Lloyd(seeds)
    #seeds = [p[0] for p in pts]
    #print("seeds == "+str(seeds))
    #print("seeds == "+str(seeds))


    #lloyd = Lloyd(all_points, center=(0,0), radius=radius)
    # seeds
    lloyd = Lloyd(seeds, center=(0,0), radius=radius)
    # We basically wan't to move the points until the points are are at the centroids of the voronoi cells.
    while True:
        # First update, then render.
        #lloyd.update()
        lloyd.update_weighted(img)
        #lloyd.update_weighted()
        turtle.clearscreen()
        lloyd.render()
        lloyd.render_delaunay() # tris = delaunay.exportTriangles()
        #time.sleep(0.1)




    return 0


if __name__=="__main__":
    exit(main())
