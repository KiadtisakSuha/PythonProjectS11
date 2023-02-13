"""""""""""

import os
import cv2
import numpy as np

IMAGES_PATH = 'images/'

def load_image(image_path):
   
    # Create the Image directory to save any plots
    if not os.path.exists(IMAGES_PATH):
        os.makedirs(IMAGES_PATH)
    coloured_image = cv2.imread(image_path)
    grey_image = cv2.cvtColor(coloured_image, cv2.COLOR_BGR2GRAY)
    #print('image matrix size: ', grey_image.shape)
   # print('\n First 5 columns and rows of the image matrix: \n', grey_image[:5, :5])
    # cv2.imwrite('TopLeft5x5.jpg', grey_image[:5, :5])
    return grey_image


def convolve2d(image, kernel):

    kernel = np.flipud(np.fliplr(kernel))

    output = np.zeros_like(image)


    image_padded = np.zeros((image.shape[0] + 2, image.shape[1] + 2))
    image_padded[1:-1, 1:-1] = image

    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
            output[y, x] = (kernel * image_padded[y: y+3, x: x+3]).sum()

    return output

input_image = load_image('Point 2_Outline.bmp')
print(input_image)
print("____________________________________")
# kernel to be used to get sharpened image
#KERNEL = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
KERNEL = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
image_sharpen = convolve2d(input_image, kernel=KERNEL)
print(image_sharpen)
#image_sharpen = image_sharpen/255
#for x in range(len(image_sharpen)):
 #   print(image_sharpen[x])
cv2.imwrite(IMAGES_PATH + 'sharpened_image.jpg', image_sharpen)
# kernel to be used for edge detection
image_edge1 = convolve2d(input_image, kernel=np.array([[-1, -1, -1], [-1, 4, -1], [-1, -1, -1]]))
cv2.imwrite(IMAGES_PATH + 'edge_detection1.jpg', image_edge1)

image_edge2 = convolve2d(input_image, kernel=np.array([[-1, 0, 1], [0, 0, 0], [1, 0, -1]]))
cv2.imwrite(IMAGES_PATH + 'edge_detection2.jpg', image_edge2)

# kernel to be used for box blur
imageboxblur = convolve2d(input_image, kernel=np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])/9.0)
cv2.imwrite(IMAGES_PATH + 'box_blur.jpg', imageboxblur)

# kernel to be used for gaussian blur
imagegaussianblur = convolve2d(input_image, kernel=np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])/16.0)
cv2.imwrite(IMAGES_PATH + 'gaussian_blur.jpg', imagegaussianblur)
    
    """""""""""
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def dilated_conv2d(inputs, filters, dilation_rate):
    sh, sw = dilation_rate
    ih, iw = inputs.shape
    oh, ow = (ih + sh - 1)//sh, (iw + sw - 1)//sw
    output = np.zeros((oh, ow))
    for y in range(oh):
        for x in range(ow):
            ii = y*sh
            jj = x*sw
            if ii >= 0 and ii < ih and jj >= 0 and jj < iw:
                output[y, x] = np.sum(inputs[ii:ii+sh, jj:jj+sw] * filters)
    return output

inputs = plt.imread("Point 2_Outline.bmp")
inputs = inputs/255
if inputs.ndim == 3:
    inputs = inputs.mean(axis=2)
filters = np.ones((2, 2))
x = dilated_conv2d(inputs, filters, (2, 2))
print(x)