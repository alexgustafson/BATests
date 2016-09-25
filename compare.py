import cv2
from skimage import measure
import utilities.start_django
from border_results.models import ProcessResult
from numpy import array
from PIL import Image
import os
from pylab import *

def result_has_mask(lesion_image):
    if lesion_image.evaluation.border_quality == 10:
        return True
    elif lesion_image.evaluation.border_quality == 20:
        return True
    elif lesion_image.mask:
        return True

    return False


def get_mask(lesion_image):
    if lesion_image.evaluation.border_quality == 10:
        return lesion_image.calculated_mask
    elif lesion_image.evaluation.border_quality == 20:
        return lesion_image.calculated_mask
    elif lesion_image.mask:
        return lesion_image.mask
    return None


lesion_images = ProcessResult.objects.filter(evaluation__border_quality=10)

for lesion_image in lesion_images:

    if result_has_mask(lesion_image):
        if os.path.exists(get_mask(lesion_image)):
            if '_lesion.bmp' in get_mask(lesion_image):
                border = array(Image.open(get_mask(lesion_image)).convert(mode='L'))
            else:
                border = array(Image.open(get_mask(lesion_image)))
        else:
            print(u'no mask found for {0}'.format(lesion_image))
            continue
    else:
        continue

    if len(border.shape)> 2:
        border = border[:,:,0]

    props = measure.regionprops(border)
    output = cv2.connectedComponentsWithStats(border, 4, cv2.CV_32S)

    regions = output[1]
    stats = output[2]

    print(lesion_image.name)

