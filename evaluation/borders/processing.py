from numpy import array
from PIL import Image
import os
from path import path
from skimage.segmentation import slic, clear_border, mark_boundaries
from skimage.color import rgb2hsv
import numpy as np
from skimage.filters import gaussian
from skimage import exposure
from skimage.io import imsave



def prep(bckgr_image, image, n_seqments=6, multichannel=False, sigma=4.1, buffer_size=25, color=[1,1,1]):


    slic_im = slic(
                image,
                n_segments=n_seqments,
                multichannel=multichannel,
                sigma=sigma,
                min_size_factor=0.05,
                compactness=10,
                max_iter=12
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


def hsv_modulation(lesion_image):

    img_path = os.path.join('../', lesion_image.path)

    if not os.path.exists(img_path):
        print('no image found: ', lesion_image.name)
        return []

    image = Image.open(img_path)
    mode = image.mode
    format = image.format
    height = image.height
    width = image.width

    image = array(image)

    if mode == 'RGBA':
        image = image[:,:,0:3]

    if lesion_image.source == 'DermQuest':
        image = image[0:-100, :]

    center = (int(height / 2), int(width / 2))
    image_hsv = rgb2hsv(image)

    sigma = image.size/800000
    oimage = np.copy(image)
    image = gaussian(image, sigma=sigma, multichannel=True)

    h = image_hsv[:,:,0]
    s = image_hsv[:,:,1]
    v = image_hsv[:,:,2]

    h = gaussian(h, sigma=sigma)
    p2, p98 = np.percentile(h, (2, 98))
    h = exposure.rescale_intensity(h, in_range=(p2, p98))

    s_inv_v = s * ((v * -1) + 1)
    s_inv_v_h = s * ((v * -1) + 1) * ((h * -1) + 1)

    slic_s = prep(oimage, s * 256)
    path_string = 'media/{0}.slic_s.jpeg'.format(lesion_image.name)
    media_path = path(path_string)

    imsave(media_path.abspath(), slic_s)

    return [{'name': 'foo'}, {'name': 'bar'}]