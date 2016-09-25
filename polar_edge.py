import cv2
from skimage import measure
import utilities.start_django
from border_results.models import ProcessResult
from numpy import array
from PIL import Image
import os
from skimage.color import rgb2hsv
from skimage.transform import rotate
import numpy as np
import matplotlib.pyplot as plt
from skimage import segmentation


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


def get_center_coordinates(np_image):
    height = int(image.shape[0]/2)
    width = int(image.shape[1]/2)
    return (height,width)


def regularize_array_lengths(arr, val=0.):

    lengths = [len(row) for row in arr]
    max_length = max(lengths)

    for i in np.arange(len(arr)):

        while len(arr[i]) < max_length:
            arr[i] = np.append(arr[i], [[0., 0., 0.]], axis=0)

    return arr



lesion_images = ProcessResult.objects.all().order_by('?')

for lesion_image in lesion_images:

    if not os.path.exists(lesion_image.original_image):
        print('no image found: ', lesion_image.name)
        continue

    image = Image.open(lesion_image.original_image)
    mode = image.mode
    format = image.format
    height = image.height
    width = image.width

    image = array(image)

    if mode == 'RGBA':
        image = image[:,:,0:3]

    #image = rgb2hsv(image)
    center = get_center_coordinates(image)

    print(u'{0} | width: {1} height : {2} center:{3}'.format(lesion_image.name, image.shape[0], image.shape[1], center))

    polar_image_1 = []
    polar_image_2 = []
    polar_image_3 = []
    polar_image_4 = []
    polar_image = []

    for i in range(0, 90):

        rotated_image = rotate(image, -i)
        center_row_h = rotated_image[center[0]]
        center_row_v = rotated_image[:, center[1]]

        polar_image_1.append(np.array_split(center_row_h, 2)[1])
        polar_image_2.append(np.array_split(center_row_v, 2)[0][::-1])
        polar_image_3.append(np.array_split(center_row_h, 2)[0][::-1])
        polar_image_4.append(np.array_split(center_row_v, 2)[1])

    polar_image = polar_image_1 + polar_image_2 + polar_image_3 + polar_image_4
    polar_image = regularize_array_lengths(polar_image)
    polar_image = np.array(polar_image)


    #fig = plt.figure(figsize=(12, 6))
    #ax = fig.add_subplot(111)
    #ax.imshow(polar_image)

    #plt.show()

    polar_image_hsv = rgb2hsv(polar_image)
    image_hsv = rgb2hsv(image)

    fig = plt.figure(figsize=(16, 16))

    ax = fig.add_subplot(331)
    ax.imshow(polar_image_hsv[:,:,0])
    ax = fig.add_subplot(332)
    ax.imshow(polar_image_hsv[:,:,1])
    ax = fig.add_subplot(333)
    ax.imshow(polar_image_hsv[:,:,2])
    ax = fig.add_subplot(334)
    ax.imshow(segmentation.felzenszwalb(polar_image_hsv))

    ax = fig.add_subplot(335)
    ax.imshow(image)

    ax = fig.add_subplot(336)
    ax.imshow(image_hsv[:,:,0])

    ax = fig.add_subplot(337)
    ax.imshow(image_hsv[:,:,1])

    ax = fig.add_subplot(338)
    ax.imshow(image_hsv[:,:,2])



    plt.show()



