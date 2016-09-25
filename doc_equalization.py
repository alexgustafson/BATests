import cv2

import utilities.start_django
from border_results.models import ProcessResult
from numpy import array
from PIL import Image
import os
from path import path
import matplotlib

import numpy as np
import matplotlib.pyplot as plt
from skimage.segmentation import slic, clear_border, mark_boundaries, felzenszwalb
from skimage.color import rgb2hsv, rgb2gray
from skimage import measure
from skimage.filters import gaussian, median
from skimage import exposure
from skimage.morphology import closing
from skimage.io import imsave
from skimage.restoration import denoise_tv_chambolle, denoise_bilateral
from skimage import data, img_as_float

def plot_img_and_hist(img, axes, bins=256):
    """Plot an image along with its histogram and cumulative histogram.

    """
    img = img_as_float(img)
    ax_img, ax_hist = axes
    ax_cdf = ax_hist.twinx()

    # Display image
    ax_img.imshow(img, cmap=plt.cm.gray)
    ax_img.set_axis_off()
    ax_img.set_adjustable('box-forced')

    # Display histogram
    ax_hist.hist(img.ravel(), bins=bins, histtype='step', color='black')
    ax_hist.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax_hist.set_xlabel('Pixel intensity')
    ax_hist.set_xlim(0, 1)
    ax_hist.set_yticks([])

    # Display cumulative distribution
    img_cdf, bins = exposure.cumulative_distribution(img, bins)
    ax_cdf.plot(bins, img_cdf, 'r')
    ax_cdf.set_yticks([])

    return ax_img, ax_hist, ax_cdf

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
    center = (int(height / 2), int(width / 2))
    sigma = image.size / 800000

    if mode == 'RGBA':
        image = image[:,:,0:3]

    if lesion_image.source == 'DermQuest':
        image = image[0:-100, :]


    gray = rgb2gray(image)
    img_eq = exposure.equalize_hist(image)

    kernel_size = int(min(height, width) / 80)
    img_adapteq = exposure.equalize_adapthist(image, kernel_size=kernel_size, clip_limit=0.01)
    #img_adapteq = exposure.equalize_adapthist(image, ntiles_x=12, ntiles_y=12, clip_limit=0.01)

    fig = plt.figure(figsize=(24, 16))
    axes = np.zeros((2, 3), dtype=np.object)
    axes[0, 0] = fig.add_subplot(2, 3, 1)
    for i in range(1, 3):
        axes[0, i] = fig.add_subplot(2, 3, 1 + i, sharex=axes[0, 0], sharey=axes[0, 0])
    for i in range(0, 3):
        axes[1, i] = fig.add_subplot(2, 3, 4 + i)

    matplotlib.rcParams['font.size'] = 18
    ax_img, ax_hist, ax_cdf = plot_img_and_hist(image[0:-100, 0:-100], axes[:, 0])
    ax_img.set_title('Original Image')
    y_min, y_max = ax_hist.get_ylim()
    ax_hist.set_ylabel('Number of pixels')
    ax_hist.set_yticks(np.linspace(0, y_max, 5))

    ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_eq[0:-100, 0:-100], axes[:, 1])
    ax_img.set_title('Histogram equalization')

    ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_adapteq[0:-100, 0:-100], axes[:, 2])
    ax_img.set_title('Adaptive equalization')



    ax_cdf.set_ylabel('Fraction of total intensity')
    ax_cdf.set_yticks(np.linspace(0, 1, 5))

    fig.subplots_adjust(wspace=0.4)



    print(u'{0} | width: {1} height : {2} center:{3}, sigma{4}'.format(lesion_image.name, image.shape[0], image.shape[1], center, sigma))

    plt.show()

