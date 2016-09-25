import cv2

import utilities.start_django
from border_results.models import ProcessResult
from numpy import array
from PIL import Image
import os
from path import path

import numpy as np
import matplotlib.pyplot as plt
from skimage.segmentation import slic, clear_border, mark_boundaries, felzenszwalb
from skimage.color import rgb2hsv
from skimage import measure
from skimage.filters import gaussian, median
from skimage import exposure
from skimage.morphology import closing
from skimage.io import imsave
from skimage.restoration import denoise_tv_chambolle, denoise_bilateral



def regularize_array_lengths(arr, val=0.):

    lengths = [len(row) for row in arr]
    max_length = max(lengths)

    for i in np.arange(len(arr)):

        while len(arr[i]) < max_length:
            arr[i] = np.append(arr[i], [[0., 0., 0.]], axis=0)

    return arr


def prep_1(bckgr_image, image, n_seqments=4, multichannel=False, sigma=4.1, buffer_size=25, color=[1,1,1]):


    slic_im = slic(
                image,
                n_segments=n_seqments,
                multichannel=multichannel,
                sigma=sigma,
                min_size_factor=0.02,
                compactness=10,
                max_iter=10
            )

    #bckgr_image = mark_boundaries(bckgr_image, slic_im, color=[0,0,1])

    return clear_border(
            slic_im,
            buffer_size=buffer_size)




def prep(bckgr_image, image, n_seqments=4, multichannel=False, sigma=4.1, buffer_size=25, color=[1,1,1]):


    slic_im = slic(
                image,
                n_segments=n_seqments,
                multichannel=multichannel,
                sigma=sigma,
                min_size_factor=0.02,
                compactness=10,
                max_iter=10
            )

    #bckgr_image = mark_boundaries(bckgr_image, slic_im, color=[0,0,1])

    return mark_boundaries(
        bckgr_image,
        clear_border(
            slic_im,
            buffer_size=buffer_size),
        color=color,
        outline_color=[1,0,0],
        mode='thick',
    )


#lesion_images = ProcessResult.objects.all().order_by('?')
lesion_images = ProcessResult.objects.filter(name="021878HB.jpeg")
#lesion_images = []


class MyImage:
    def __init__(self):
        self.path = ""
        self.source = ""
        self.name = ""


#image = MyImage()
#image.path = '/Users/alexandergustafson/Desktop/lesion.jpg'
#lesion_images.append(image)

for lesion_image in lesion_images:

    if not os.path.exists(lesion_image.path):
        print('no image found: ', lesion_image.name)
        continue

    image = Image.open(lesion_image.path)
    mode = image.mode
    format = image.format
    height = image.height
    width = image.width

    image = array(image)

    if mode == 'RGBA':
        image = image[:,:,0:3]

    image = image[0:-100, 0:-100]

    center = (int(height/2), int(width/2))

    image_hsv = rgb2hsv(image)

    fig = plt.figure(figsize=(16, 12))

    ax = fig.add_subplot(221)
    ax.imshow(image[200:-100, 200:-300])

    path_string = '/Users/alexandergustafson/Desktop/original.jpeg'
    media_path = path(path_string)
    imsave(media_path.abspath(), image[200:-100, 200:-300])


    sigma = image.size/800000
    oimage = np.copy(image)

    image = gaussian(image, sigma=2*sigma/3, multichannel=True)

    kernel_size = int(min(height, width) / 80)
    image = exposure.equalize_adapthist(image, kernel_size=kernel_size)

    ax = fig.add_subplot(222)
    ax.imshow(image[200:-100, 200:-300])

    path_string = '/Users/alexandergustafson/Desktop/clean.jpeg'
    media_path = path(path_string)
    imsave(media_path.abspath(), image[200:-100, 200:-300])

    ax = fig.add_subplot(223)
    ax.set_title('slic(image)')
    slic_img = prep_1(oimage[200:-100, 200:-300], image[200:-100, 200:-300], multichannel=True, sigma=sigma/2)
    ax.imshow(slic_img)
    mask = np.zeros((730,1040,3), dtype="uint8")
    mask[slic_img == 0] = [0,0,0]
    mask[slic_img > 0] = [255,0,0]
    path_string = '/Users/alexandergustafson/Desktop/segement.jpeg'
    media_path = path(path_string)
    imsave(media_path.abspath(), mask)

    ax = fig.add_subplot(224)
    slic_img = prep(oimage[200:-100, 200:-300], image[200:-100, 200:-300], multichannel=True, sigma=sigma/2)
    ax.imshow(slic_img)
    path_string = '/Users/alexandergustafson/Desktop/process.jpeg'
    media_path = path(path_string)
    imsave(media_path.abspath(), slic_img)

    print(u'{0} | width: {1} height : {2} center:{3}, sigma{4}'.format(lesion_image.name, image.shape[0], image.shape[1], center, sigma))

    plt.show()


