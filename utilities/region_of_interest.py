from skimage.segmentation import mark_boundaries
from skimage import color
from pylab import *
import cv2
from skimage import img_as_ubyte, img_as_uint



def get_region(image, mask):
    if len(mask.shape) > 2:
        ret, mask = cv2.threshold(mask[:, :, 0], 1, 255, cv2.THRESH_BINARY)
    else:
        ret, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

    masked = cv2.bitwise_and(image, image, mask=mask)

    return masked
