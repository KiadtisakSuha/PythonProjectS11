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

'''import cv2
import matplotlib.pyplot as plt

# Load an example image
image = cv2.imread("Point1_Template.bmp")

# Convert the image to the LAB color space
lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Apply mean shift segmentation
shifted_image = cv2.pyrMeanShiftFiltering(lab_image, 21, 51)

# Convert the shifted image back to RGB color space
shifted_image = cv2.cvtColor(shifted_image, cv2.COLOR_BGR2RGB)

# Display the original and shifted images
fig, ax = plt.subplots(ncols=2, figsize=(8, 4))
ax[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
ax[0].set_title("Original")
ax[1].imshow(cv2.cvtColor(shifted_image, cv2.COLOR_BGR2RGB)) s
ax[1].set_title("Shifted")
plt.show()'''
from time import sleep
from threading import Thread
from _thread import interrupt_main
from signal import signal
from signal import SIGINT
import sys


def handle_sigint(signalnum, frame):
    print("xxx")

class common():
    def __init__(self,target,Time):
        self.target = target
        self.Time = Time
        signal(SIGINT, target)
        thread = Thread(target=self.task)
        thread.start()
    def task(self):
        sleep(self.Time)
        thread = Thread(target=self.task)
        thread.start()
        interrupt_main()

common(handle_sigint,1)
while True:
    print("Ball")
    sleep(1)