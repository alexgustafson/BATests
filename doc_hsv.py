import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import utilities.start_django
from border_results.models import ProcessResult

from PIL import Image

from skimage.segmentation import slic, clear_border, mark_boundaries, felzenszwalb
from skimage.color import rgb2hsv
from skimage import exposure
from skimage.morphology import disk
from pylab import *


def transform_to_hsv_space(im):

    fig = plt.figure(figsize=(12, 6))

    ax = fig.add_subplot(121)
    ax.imshow(im)
    ax.set_title('Original Image')

    ax = fig.add_subplot(122, projection='3d')

    #im = rgb2hsv(im)
    index = 0

    # loop through pixels array and add each pixel as item in scatter plot
    for row in im:
        for pixel in row:
            index = index + 1
            if index % 80 > 0:
                continue
            [[(H, S, V)]] =  rgb2hsv([[pixel]])
            x = cos(H*2*pi) * S
            y = sin(-H*2*pi) * S
            z = V
            color = (pixel[0]/255.,pixel[1]/255.,pixel[2]/255.)
            marker = ','

            ax.scatter(x,y,z,c=color, s=10, lw = 0, alpha=0.08)
    ax.set_zlabel('V')
    ax.view_init(elev=17., azim=30)
    ax.set_title('Image in HSV Space')
    plt.show()

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
#lesion_images = ProcessResult.objects.filter(source='DermQuest').order_by('?')
lesion_images = ProcessResult.objects.filter(name__in=['020254HB.JPG','021837HB.jpeg','020266HB.JPG','020319HB.JPG'])
#lesion_images = ProcessResult.objects.filter(name="021878HB.jpeg")
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
    oimage = np.copy(image)

    center = (int(height / 2), int(width / 2))
    sigma = image.size / 800000
    size = image.size
    disk_size = int(size/500000)
    disk_size = max(disk_size, 2) +1

    if mode == 'RGBA':
        image = image[:,:,0:3]

    if lesion_image.source == 'DermQuest':
        image = image[0:-100, :]

    transform_to_hsv_space(image)

    kernel_size = int(min(height, width) / 80)
    image = exposure.equalize_adapthist(image, kernel_size=kernel_size, clip_limit=0.01)
    image[:,:,0] = median(image[:,:,0], disk(disk_size))
    image[:,:,1] = median(image[:,:,1], disk(disk_size))
    image[:,:,2] = median(image[:,:,2], disk(disk_size))


    image = image[200:-200, 200:-200]

    hsv_image = rgb2hsv(image)
    h = hsv_image[:,:,0]
    s = hsv_image[:,:,1]
    v = hsv_image[:,:,2]

    s_inv_v = s * ((v * -1))
    s_inv_v_h = s * ((v * -1) + 1) * ((h * -1) + 1)

    fig = plt.figure(figsize=(16, 6))

    ax = fig.add_subplot(241)
    ax.set_title('original image', fontsize=20)
    ax.imshow(oimage)

    ax = fig.add_subplot(242)
    thresh = 100
    ax.set_title('hue', fontsize=20)
    ax.imshow(hsv_image[:,:,0])

    ax = fig.add_subplot(243)
    ax.set_title('saturation', fontsize=20)
    ax.imshow(hsv_image[:,:,1])

    ax = fig.add_subplot(244)
    ax.set_title('value', fontsize=20)
    ax.imshow(hsv_image[:,:,2])

    ax = fig.add_subplot(245)
    ax.set_title('s * inv(v)', fontsize=20)
    ax.imshow(s_inv_v)


    print(u'{0} | width: {1} height : {2} center:{3}, sigma{4}'.format(lesion_image.name, image.shape[0], image.shape[1], center, sigma))

    plt.show()


