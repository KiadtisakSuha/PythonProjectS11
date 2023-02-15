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
import os
import json
class ReadFile:
    @staticmethod
    def ReadFile_Score(PartNumber,Couter_Point):
            with open(PartNumber + '/' + PartNumber + '.json', 'r') as json_file:
                Master = json.loads(json_file.read())
            print(Couter_Point,len(Master))
            if Couter_Point == len(Master):
                if Couter_Point != 0:
                    Point_Left = []
                    Point_Top = []
                    Point_Right = []
                    Point_Bottom = []
                    Point_Score = []
                    Point_Mode = []
                    Point_Color = []
                    Color = []
                    for Point in range(Couter_Point):
                        FileFolder_Ok = 'Record/' + PartNumber + '/OK/Point' + str(Point +  1)
                        path = os.path.join(FileFolder_Ok)
                        try:
                            os.makedirs(path, exist_ok=True)
                        except OSError as error:
                            pass
                        FileFolder_NG = 'Record/' + PartNumber + '/NG/Point' + str(Point + 1)
                        path = os.path.join(FileFolder_NG)
                        try:
                            os.makedirs(path, exist_ok=True)
                        except OSError as error:
                            pass
                        Point_Mode.append(Master[Point]["Point" + str(Point + 1)][0]["Mode"])
                        Point_Left.append(Master[Point]["Point" + str(Point + 1)][0]["Left"])
                        Point_Top.append(Master[Point]["Point" + str(Point + 1)][0]["Top"])
                        Point_Right.append(Master[Point]["Point" + str(Point + 1)][0]["Right"])
                        Point_Bottom.append(Master[Point]["Point" + str(Point + 1)][0]["Bottom"])
                        Point_Score.append(Master[Point]["Point" + str(Point + 1)][0]["Score"])
                        Point_Color.append(Master[Point]["Point" + str(Point + 1)][0]["Color"])
                        Color.append("#A9A9A9")
                    return Point_Left,Point_Top,Point_Right,Point_Bottom,Point_Score,Point_Mode,Point_Color,Color
                    #return Point_Mode,Point_Left,Point_Top,Point_Right,Point_Bottom,Point_Score,Point_Color,Color



Pt = "TMTD894LOO"
couter = 2
print(ReadFile.ReadFile_Score(Pt,couter))