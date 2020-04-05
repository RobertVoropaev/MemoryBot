import numpy as np
import cv2 as cv

def denoizing_img(img_name):
    img = cv.imread('data/1.jpg')
    img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

    dst = cv.fastNlMeansDenoisingColored(src=img, dst=None, h=10, hColor=10,
                                         templateWindowSize=7, searchWindowSize=21)

