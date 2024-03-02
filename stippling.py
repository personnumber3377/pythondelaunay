
import sys
from lloyd import *
from image_helper import *
import random
from util import *
import turtle

def main(): # Loads an image called image.png and then shows the voronoi stippling of that image.
    if len(sys.argv) == 1: # One argument only.
        image_file = "image.png"
    else:
        image_file = sys.argv[-1] # Get the last file.
    print("Loading file: "+str(image_file))
    img = load_image(image_file)

    radius = 1


    # Now create the points for areas which are dark.
    pts = []
    all_points = []

    #point_count = 100

    #point_count = 6000

    point_count = 2000

    #for i in range(len(img)):
    #    cur_line = []
    #    for j in range(len(img[0])):
    

    BRIGHTNESS_TRESHOLD = 100 # Maximum brightness to consider a point.

    while point_count:
        i = random.randrange(len(img))
        j = random.randrange(len(img[0]))
        # The current pixel is img[i][j] and should be a flat list of length three (or maybe four)???
        pix = img[i][j]
        assert len(pix) == 4 or len(pix) == 3
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
        if brightness < BRIGHTNESS_TRESHOLD: # We want DARK spots, not light spots. Therefore less than.
            actual_point = (((i/(len(img)))*radius*2-(radius), j/(len(img[0]))*radius*2-(radius)), brightness) # How far along the x coordinates we are times the radius giving us the correct place.
            # Sanity checks.
            # The point should not be outside of the bounding box.

            x = actual_point[0][0]
            y = actual_point[0][1]
            #print("x == "+str(x))
            #print("y == "+str(y))
            assert x >= -1*radius and x <= radius and y >= -1*radius and y <= radius # Sanity
            #print("Point passed!!!")
            #cur_line.append(actual_point)
            all_points.append(actual_point[0])
        #pts.append(cur_line)
        point_count -= 1
    

    #radius += 3

    print("Processed image")
    # Ok, so I have every pixel, which is dark enough in the pts list. it is time to update the stuff.
    # Now finally do the stuff

    # First generate testdata:
    numSeeds = 50
    #radius = 50 # Set the radius to a big number.

    # Now set the radius shit.

    #radius = max(len(img), len(img[0]))

    #seeds = radius * np.random.random((numSeeds, 2))
    # subtract half of radius from each point to get the shit
    seeds = []
    for _ in range(numSeeds):
        orig_point = 2*radius * np.array([random.random(), random.random()])
        # Now subtract one radius.
        orig_point[0] = orig_point[0] - radius
        orig_point[1] = orig_point[1] - radius
        #print("x == "+str(x))
        print("orig_point == "+str(orig_point))
        x = orig_point[0]
        y = orig_point[1]
        assert x >= -1*radius and x <= radius
        assert y >= -1*radius and y <= radius
        seeds.append(orig_point)
    # Crate a group of points, (centered at 0,0)


    #seeds = radius * (np.random.random((numSeeds, 2))- np.array([-1/2*radius, -1/2*radius]))


    #seeds = radius * np.random.random((numSeeds, 2))
    #seeds = [(10,0),(-10,0),(0,-10),(0,10),(10,10)]
    #seeds = [(x*5,x) for x in range(-5,5,1)]
    #seeds = [(-10,0), (10,0), (10,10)]
    #seeds = [(-10,0), (10,0), (0,10)]
    # First declare the Lloyd object.
    #lloyd = Lloyd(seeds)
    #seeds = [p[0] for p in pts]
    #print("seeds == "+str(seeds))
    #print("seeds == "+str(seeds))
    #seeds = [(-10,0), (10,0), (0,10)]

    #seeds = [(0,0)]
    print("seeds: "+str(seeds))

    #lloyd = Lloyd(all_points, center=(0,0), radius=radius)
    # seeds
    #lloyd = Lloyd(seeds, center=(0,0), radius=radius)
    # all_points
    #all_points = [(31.935483870967744, 33.5), (16.451612903225808, -48.0), (-39.67741935483871, -16.5), (43.54838709677419, 45.5), (-17.741935483870968, -20.0), (35.80645161290322, 23.5), (-23.548387096774192, -41.5), (-22.258064516129032, -30.5), (26.77419354838709, 37.5), (-18.38709677419355, 12.5), (-5.483870967741936, 11.0), (43.54838709677419, -44.0), (-2.258064516129032, 32.0), (26.77419354838709, 25.0), (-0.32258064516128826, 20.5), (-41.61290322580645, 35.5), (-42.25806451612903, -14.0), (8.064516129032263, 48.5), (31.290322580645153, 49.5), (21.612903225806463, 14.0), (-40.96774193548387, 26.0), (35.16129032258064, 37.0), (-40.32258064516129, -46.5), (-46.12903225806451, 21.0), (-42.25806451612903, -2.5), (28.064516129032256, 24.5), (-6.1290322580645125, -35.0), (38.38709677419355, -48.0), (-48.70967741935484, 10.0), (-26.774193548387096, -49.0), (-8.064516129032256, 32.0), (8.064516129032263, -46.0), (-40.32258064516129, 41.5), (25.483870967741936, -36.0), (11.935483870967744, -8.0), (35.80645161290322, -34.5), (21.612903225806463, -43.5), (31.290322580645153, 44.5), (-37.74193548387097, -13.0), (46.12903225806451, -10.5), (-35.806451612903224, -37.5), (-42.25806451612903, -46.0), (31.935483870967744, -34.5), (-41.61290322580645, -3.5), (-36.45161290322581, -35.5), (-19.032258064516128, -31.5), (-39.67741935483871, -46.0), (25.483870967741936, -46.5), (-2.258064516129032, 17.5), (-41.61290322580645, -43.0), (41.61290322580645, -44.5), (-33.2258064516129, -38.5), (-22.258064516129032, 2.5), (15.806451612903231, -14.5), (41.61290322580645, 13.0), (-49.354838709677416, -34.5), (15.806451612903231, 20.5), (-46.774193548387096, -37.5), (46.12903225806451, -32.0), (-30.64516129032258, 33.5)]
    


    # Here is the crashing input.

    #all_points = [(29.354838709677423, 39.5), (29.354838709677423, 44.5), (14.516129032258064, 22.5), (-35.806451612903224, 46.0), (-11.29032258064516, 17.5), (33.87096774193549, -3.0), (4.838709677419352, -46.5), (46.12903225806451, 16.0), (8.064516129032263, -48.5), (-29.35483870967742, 40.0), (25.483870967741936, 31.0), (-39.03225806451613, 15.0), (-22.90322580645161, -22.499999999999996), (-11.29032258064516, 0.0), (-10.0, 10.5), (26.77419354838709, -31.5), (-20.322580645161292, 6.999999999999993), (30.0, -46.0), (-13.225806451612904, -33.0), (-17.741935483870968, -21.000000000000004), (-27.41935483870968, -34.0), (-30.0, -31.0), (49.35483870967742, -41.0), (-44.193548387096776, -38.5), (-25.483870967741936, -43.5), (-27.41935483870968, 45.5), (48.064516129032256, -5.0), (-9.354838709677423, -42.5), (31.290322580645153, -18.0), (25.483870967741936, 36.0), (-24.193548387096776, 48.5), (42.903225806451616, 30.0), (-8.70967741935484, -37.0), (23.548387096774192, 23.5), (28.709677419354847, 23.5), (-32.58064516129032, 47.5), (-39.03225806451613, 17.5), (-50.0, -43.0), (35.80645161290322, -43.0), (14.516129032258064, -10.5), (18.38709677419355, 23.5), (-11.29032258064516, 9.0), (0.32258064516128826, -49.5), (-10.0, 28.0), (-37.74193548387097, -38.5), (-43.54838709677419, -46.0), (11.935483870967744, -45.0), (27.41935483870968, -38.0), (-4.838709677419359, -41.0), (14.516129032258064, -14.5), (6.774193548387096, -12.0), (42.25806451612904, 42.0)]




    print("Here is all_points: "+str(all_points))
    
    #cur_point = random.choice(all_points)
    #all_points = [(-5.483870967741936, 11.0), (-0.32258064516128826, 20.5)]
    #all_points = [(-5.483870967741936, 11.0), (-46.12903225806451, 21.0), (-26.774193548387096, -49.0), (35.80645161290322, -34.5), (-30.64516129032258, 33.5)]
    FUZZ_CRASH = False


    #all_points = [(29.354838709677423, 44.5), (-35.806451612903224, 46.0), (-11.29032258064516, 0.0), (-10.0, 10.5), (-20.322580645161292, 6.999999999999993), (-27.41935483870968, -34.0), (49.35483870967742, -41.0), (-44.193548387096776, -38.5), (25.483870967741936, 36.0), (23.548387096774192, 23.5), (-10.0, 28.0), (14.516129032258064, -14.5)]

    #all_points = [(-35.806451612903224, 46.0), (-11.29032258064516, 0.0), (-10.0, 10.5), (-20.322580645161292, 6.999999999999993), (49.35483870967742, -41.0), (-44.193548387096776, -38.5), (25.483870967741936, 36.0), (23.548387096774192, 23.5), (-10.0, 28.0), (14.516129032258064, -14.5)]



    # This is the smallest testcase:

    #all_points = [(-11.29032258064516, 0.0), (-20.322580645161292, 6.999999999999993), (49.35483870967742, -41.0), (-44.193548387096776, -38.5), (25.483870967741936, 36.0), (23.548387096774192, 23.5), (-10.0, 28.0), (14.516129032258064, -14.5)]

    #all_points = [(-0.6129032258064516, -0.95), (-0.2645161290322581, -0.98), (0.7032258064516128, 0.3799999999999999), (0.9225806451612903, -1.0), (0.8838709677419354, 0.30000000000000004), (-0.29032258064516125, 0.5900000000000001), (0.3677419354838709, 0.31000000000000005), (0.49677419354838714, 0.8200000000000001), (-0.5612903225806452, -0.98), (-0.3548387096774194, -0.99)]

    #render_points(all_points, color="red")
    #render_polygon(all_points, color="blue")
    #turtle.update()
    #time.sleep(2)


    #lloyd = Lloyd(all_points, center=(0,0), radius=radius)

    #all_points = [(0.9225806451612903, 0.3999999999999999), (-0.13548387096774195, 0.20999999999999996), (-0.7677419354838709, 0.52), (0.9741935483870967, -0.26), (0.9741935483870967, -0.26), (0.9096774193548387, 0.6599999999999999), (0.9096774193548387, -0.36), (0.07096774193548394, 0.5900000000000001), (0.43225806451612914, 0.28), (0.8709677419354838, 0.74), (-0.6774193548387097, -0.19999999999999996), (0.7161290322580645, 0.8200000000000001)]

    #assert not check_multiple(all_points)


    if FUZZ_CRASH:
        global EXCEPTION
        while True:
            random_index = random.randrange(0, len(all_points))
            #print("random_index == "+str(random_index))
            print("Here is the current point list: "+str(all_points))
            print("Here is the length of the point list: "+str(len(all_points)))
            try:
                # First try removing the point.
                orig_len = len(all_points)
                removed_point = all_points.pop(random_index)
                #removed_point = all_points[0]

                lloyd = Lloyd(all_points, center=(0,0), radius=radius)
                '''
                if EXCEPTION:
                    # Exception:
                    print("We found the exception!!!")
                    # Just remove and continue
                    continue
                else:
                    # No exception
                    print("No exception!!!")
                    exit(1)
                    # No exception, therefore add the point back in.
                '''

                # No exception!!! Put the point back
                all_points.insert(random_index, removed_point)
                assert len(all_points) == orig_len
            

            except AssertionError:
                # This is actually the assertion which we want
                print("Exception!!!")
                #exit(1)
                # Add point back in because we got an exception which we didn't really want and continue.


                #all_points.insert(random_index, removed_point)

                #exit(1)
            #continue


    lloyd = Lloyd(all_points, center=(0,0), radius=radius)

    # all_points
    #lloyd = Lloyd(all_points, center=(0,0), radius=radius)
    # We basically wan't to move the points until the points are are at the centroids of the voronoi cells.
    t = turtle.Turtle()
    while True:
        # First update, then render.
        #lloyd.update()
        '''
        try:
            lloyd.update_weighted(img)
        except:
            
            print("Exception!!")
            assert False
            exit(1)
        '''

        lloyd.update_weighted(img)
        turtle.clearscreen()
        lloyd.render()
        # lloyd.debug_polygon_shit()  # Just for debug.
        lloyd.render_voronoi_debug(t)
        #lloyd.render_delaunay() # tris = delaunay.exportTriangles()
        turtle.update()
        #time.sleep(4)
        time.sleep(0.3)



    return 0


if __name__=="__main__":
    exit(main())
