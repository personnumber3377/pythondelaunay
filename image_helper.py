
from PIL import Image
import numpy as np

def load_image(path):


    image = Image.open(path)
    input_array = np.asarray(image)

    
    #output_image.save("test_result.png")
    return input_array # Returns a height * width * 3 dimensional matrix.

