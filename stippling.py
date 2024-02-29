
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
    for i in range(len(img)):
        for j in range(len(img[0])):
            # The current pixel is img[i][j] and should be a flat list of length three (or maybe four)???
            pix = img[i][j]
            assert len(pix) == 4 or len(pix) == 2
            print("Here is the pixel: "+str(pix))
            # Get brightness
            brightness = (pix[0]+pix[1]+pix[2])/3.0
            if brightness < 100: # We want DARK spots, not light spots. Therefore less than.
                actual_point = ((i/(len(img)))*r*2-(r), j/(len(img[0]))*r*2-(r)) # How far along the x coordinates we are times the radius giving us the correct place.
                # Sanity checks.
                # The point should not be outside of the bounding box.
                x = actual_point[0]
                y = actual_point[1]
                assert x >= -1*r and x <= r and y >= -1*r and y <= r
                print("Point passed!!!")
    
    return 0


if __name__=="__main__":
    exit(main())
