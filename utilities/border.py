from utilities.images import all_images, ImageItem, ImageProcessResults
from skimage.segmentation import slic
from skimage import img_as_ubyte, img_as_uint
from skimage.io import imsave
from pylab import *
import cv2
from path import path
from skimage.segmentation import mark_boundaries


def crop_to_center(image, scale=1.0):
    if scale == 1.0:
        return image
    else:
        height = int(image.shape[0] * scale)
        width = int(image.shape[1] * scale)
        top = int(image.shape[0] / 2) - int(height / 2)
        left = int(image.shape[1] / 2) - int(width / 2)

    return image[top:top + height, left:left + width]


def select_region_closest_to_center(mask, original, scale=1.0):
    mask = crop_to_center(mask, scale)
    original = crop_to_center(original, scale)

    output = cv2.connectedComponentsWithStats(img_as_ubyte(mask), 4, cv2.CV_32S)

    regions = output[1]

    # find region at to center
    center = (int(mask.shape[0] / 2), int(mask.shape[1] / 2))
    center_id = regions[center]
    distance = 0
    while center_id == 0:
        distance += 1
        for x in range(-distance,distance,1):
            for y in range(-distance, distance, 1):
                if center_id > 0:
                    break
                test_coord = (center[0] + x, center[1] + y)
                center_id = regions[test_coord]

            if center_id > 0:
                break


    region = regions == center_id
    kernel = np.ones((9, 9), np.uint8)
    region = cv2.dilate(img_as_ubyte(region), kernel, iterations=2)

    output = cv2.connectedComponentsWithStats(img_as_ubyte(region), 4, cv2.CV_32S)
    stats = output[2]

    padding = 25

    top = stats[1][1] - padding
    left = stats[1][0] - padding
    width = stats[1][2] + (padding * 2)
    height = stats[1][3] + (padding * 2)
    bottom = top + height
    right = left + width

    crop_box = (
        top, bottom,
        left, right,
    )

    region = region[
                top:bottom,
                left:right
             ]
    original = original[
                top:bottom,
                left:right
               ]

    return region, original, crop_box


def get_bounding_box(img):
    output = cv2.connectedComponentsWithStats(img_as_ubyte(img), 4, cv2.CV_32S)
    stats = output[2]
    box = (
        stats[1][0],
        stats[1][1],
        stats[0][2] - (stats[1][0] + stats[1][2]),
        stats[0][3] - (stats[1][1] + stats[1][3]),
    )
    return box

def test_centermost_region_touches_edges(regions):
    return False


def find_border(image_original, threshold=0.26, debug=False):


    image = image_original.get_image_data()
    shape = image.shape
    filename = image_original.name
    process_log = ImageProcessResults(shape)
    image_original.set_process_results(process_log)

    image_lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))  # Contrast Limited Adaptive Histogram Equalization
    v_eq = clahe.apply(image_lab[:, :, 0])

    image_lab[:, :, 0] = v_eq

    image_lab = cv2.cvtColor(image_lab, cv2.COLOR_LAB2RGB)

    im = cv2.medianBlur(image_lab, 9)
    im = cv2.GaussianBlur(im, (21, 21), 0)


    if debug:

        imsave(path('debug_results/{0}'.format(filename)).abspath(), image_original.get_image_data())
        #(path('debug_results/{0}.A_preprocessed_01.jpeg'.format(filename)).abspath(), image_lab)
        #imsave(path('debug_results/{0}.A_preprocessed_02.jpeg'.format(filename)).abspath(), im)
        #imsave(path('debug_results/{0}.A_preprocessed_L.png'.format(filename)).abspath(), im[:,:,0])


    size_index = 0
    increment = 5
    thresh = 70.0

    #im = cv2.cvtColor(im, cv2.COLOR_RGB2LAB)
    while size_index < threshold:
        ret, mask = cv2.threshold(im[:, :, 0], thresh, 255, cv2.THRESH_BINARY)
        output = cv2.connectedComponentsWithStats(img_as_ubyte(255 - mask), 4, cv2.CV_32S)
        regions = output[1]

        regions, foreground = remove_edge_regions(regions)

        mask_size = bincount(mask.ravel())
        size_index = mask_size[0] / (shape[0] * shape[1])

        if debug:
            imsave(path('debug_results/{0}.B_threshold_{1}.png'.format(filename, thresh)).abspath(), regions)

        process_log.log_index_threshold(size_index, thresh)
        thresh = thresh + increment


    mask = 255 - mask
    scale = 1.0

    region, im, crop_box = select_region_closest_to_center(mask, im, scale)
    cropped_original = image[crop_box[0]:crop_box[1],crop_box[2]:crop_box[3]]

    if debug:
        imsave(path('debug_results/{0}.C_center_region.png'.format(filename)).abspath(), region)

    ret, mask = cv2.threshold(img_as_ubyte(region), 1, 255, cv2.THRESH_BINARY)

    segments = 2
    forecount = 0

    while forecount == 0:

        border = slic(
            im,
            n_segments=segments,
            compactness=25,
            sigma=5.0,
        )

        border, foreground = remove_edge_regions(border)

        forecount = bincount(foreground.ravel())
        if forecount.size == 1:
            forecount = 0
        else:
            forecount = forecount[1]


        segments += 1

    masked = cv2.bitwise_and(cropped_original, cropped_original, mask=mask)

    if debug:
        imsave(path('debug_results/{0}.D_cropped.png'.format(filename)).abspath(), cropped_original)
        imsave(path('debug_results/{0}.E_border.png'.format(filename)).abspath(), border)
        #imsave(path('debug_results/{0}.F_mask.png'.format(filename)).abspath(), mask)
        #imsave(path('debug_results/{0}.G_masked.png'.format(filename)).abspath(), masked)
        imsave(path('debug_results/{0}.H_boundery.png'.format(filename)).abspath(), mark_boundaries(cropped_original, border))

    return border, mask, cropped_original, masked



def remove_edge_regions(regions):

    shape = regions.shape

    for y in range(0, shape[0], 2):
        background_id = regions[y][0]
        background = regions[:, :] == background_id
        regions[background] = 0

        background_id = regions[y][shape[1] - 1]
        background = regions[:, :] == background_id
        regions[background] = 0

    for x in range(0, shape[1], 2):
        background_id = regions[0][x]
        background = regions[:, :] == background_id
        regions[background] = 0

        background_id = regions[shape[0] - 1][x]
        background = regions[:, :] == background_id
        regions[background] = 0

    foreground = regions[:, :] > 0
    regions[foreground] = 255

    return regions, foreground