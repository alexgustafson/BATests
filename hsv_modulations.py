import cv2

import utilities.start_django
from border_results.models import ProcessResult
from numpy import array
from PIL import Image
import os

import numpy as np
import matplotlib.pyplot as plt
from skimage.segmentation import slic, clear_border, mark_boundaries, felzenszwalb
from skimage.color import rgb2hsv
from skimage import measure
from skimage.filters import gaussian
from skimage import exposure
from skimage.morphology import closing




def regularize_array_lengths(arr, val=0.):

    lengths = [len(row) for row in arr]
    max_length = max(lengths)

    for i in np.arange(len(arr)):

        while len(arr[i]) < max_length:
            arr[i] = np.append(arr[i], [[0., 0., 0.]], axis=0)

    return arr


def prep(bckgr_image, image, n_seqments=5, multichannel=False, sigma=4.1, buffer_size=25, color=[1,1,1]):


    slic_im = slic(
                image,
                n_segments=n_seqments,
                multichannel=multichannel,
                sigma=sigma,
                min_size_factor=0.05,
                compactness=10,
                max_iter=20
            )

    bckgr_image = mark_boundaries(bckgr_image, slic_im, color=[0,0,1])

    return mark_boundaries(
        bckgr_image,
        clear_border(
            slic_im,
            buffer_size=buffer_size),
        color=color,
        outline_color=[1,0,0],
        mode='thick',
    )


lesion_images = ProcessResult.objects.all().order_by('?')
#lesion_images = ProcessResult.objects.filter(name="019542VB.JPG")

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

    if lesion_image.source == 'DermQuest':
        image = image[0:-100, :]

    center = (int(height/2), int(width/2))

    image_hsv = rgb2hsv(image)

    fig = plt.figure(figsize=(16, 12))

    ax = fig.add_subplot(341)
    ax.imshow(image)

    sigma = image.size/800000
    oimage = np.copy(image)
    image = gaussian(image, sigma=sigma, multichannel=True)
    #image = exposure.equalize_adapthist(image, clip_limit=0.03)
    #image = median(image, selem=None)

    h = image_hsv[:,:,0]
    s = image_hsv[:,:,1]
    v = image_hsv[:,:,2]

    h = gaussian(h, sigma=sigma)
    p2, p98 = np.percentile(h, (2, 98))
    h = exposure.rescale_intensity(h, in_range=(p2, p98))

    s_inv_v = s * ((v * -1) + 1)
    s_inv_v_h = s * ((v * -1) + 1) * ((h * -1) + 1)

    ax = fig.add_subplot(342)
    ax.set_title('inv(H+)')
    ax.imshow((h*-1)+1)

    ax = fig.add_subplot(343)
    ax.set_title('S')
    ax.imshow(s)

    ax = fig.add_subplot(344)
    ax.set_title('inv(V)')
    ax.imshow((v*-1)+1)

    ax = fig.add_subplot(345)
    ax.set_title('S * inv(V)')
    ax.imshow(s_inv_v)

    ax = fig.add_subplot(346)
    ax.set_title('slic(s)')
    ax.imshow(prep(oimage, s * 256))

    ax = fig.add_subplot(347)
    ax.set_title('slic(s * inv(v)')
    ax.imshow(prep(oimage, s_inv_v * 256))

    ax = fig.add_subplot(348)
    ax.set_title('slic(v)')
    ax.imshow(prep(oimage, v * 256))

    ax = fig.add_subplot(349)
    ax.set_title('slic(image)')
    ax.imshow(prep(oimage, image, multichannel=True))

    ax = fig.add_subplot(3,4,10)
    ax.set_title('s * inv(v) * inv(h)')
    ax.imshow(s_inv_v_h * 256)

    ax = fig.add_subplot(3,4,11)
    ax.set_title('slic(s * inv(v) * inv(h)')
    ax.imshow(prep(oimage, s_inv_v_h * 256))

    ax = fig.add_subplot(3,4,12)
    ax.set_title('slic(H+')
    ax.imshow(prep(oimage, h * 256))

    print(u'{0} | width: {1} height : {2} center:{3}, sigma{4}'.format(lesion_image.name, image.shape[0], image.shape[1], center, sigma))

    plt.show()


