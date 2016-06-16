from utilities.images import all_images
from skimage.segmentation import slic
from skimage import img_as_ubyte
from pylab import *
import cv2

def crop_to_center(image, scale=1.0):
    if scale == 1.0:
        return image
    else:
        height = int(image.shape[0] * scale)
        width = int(image.shape[1] * scale)
        top = int(image.shape[0] / 2) - int(height / 2)
        left = int(image.shape[1] / 2) - int(width / 2)

    return image[top:top + height, left:left + width]


def find_border(image_original, region_scale=1.0, threshold=0.23):
    image = crop_to_center(image_original, region_scale)
    shape = image.shape

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))  # Contrast Limited Adaptive Histogram Equalization
    v_eq = clahe.apply(image_hsv[:, :, 2])  # Apply Equalization to Value Channel of LAB image
    s_eq = clahe.apply(image_hsv[:, :, 1])

    image_hsv[:, :, 2] = v_eq
    image_hsv[:, :, 1] = s_eq

    # merged = v_eq * s_eq

    im = cv2.medianBlur(v_eq, 9)
    im = cv2.GaussianBlur(im, (21, 21), 0)

    size_index = 0
    increment = 5
    fudge = 0.0

    while size_index < threshold:
        ret, mask = cv2.threshold(im, fudge, 255, cv2.THRESH_BINARY)
        mask_size = bincount(mask.ravel())
        size_index = mask_size[0] / (shape[0] * shape[1])
        fudge = fudge + increment

    mask = 255 - mask
    distances_from_boundary = (100, 100, 100, 100)
    scale = 1.0

    while min(distances_from_boundary) > 50:
        region, cropped, distances_from_boundary = select_region_closest_to_center(mask, image, scale)
        scale -= 0.08

    ret, mask = cv2.threshold(img_as_ubyte(region), 1, 255, cv2.THRESH_BINARY)

    return slic(cropped, n_segments=2, compactness=10, sigma=1), mask, cropped, cv2.bitwise_and(cropped, cropped, mask=mask)


def select_region_closest_to_center(mask, original, scale=1.0):
    mask = crop_to_center(mask, scale)
    original = crop_to_center(original, scale)

    output = cv2.connectedComponentsWithStats(img_as_ubyte(mask), 4, cv2.CV_32S)

    regions = output[1]

    # find region closest to center
    center = (int(mask.shape[0] / 2), int(mask.shape[1] / 2))
    center_id = regions[center]
    region = regions == center_id
    kernel = np.ones((15, 15), np.uint8)
    region = cv2.dilate(img_as_ubyte(region), kernel, iterations=2)


    output = cv2.connectedComponentsWithStats(img_as_ubyte(region), 4, cv2.CV_32S)
    stats = output[2]

    distances_from_boundary = (
        stats[1][0],
        stats[1][1],
        stats[0][2] - (stats[1][0] + stats[1][2]),
        stats[0][3] - (stats[1][1] + stats[1][3]),
    )

    region = region[
             stats[1][1] - 10:stats[1][1] + stats[0][3] + 10,
             stats[1][0] - 10:stats[1][0] + stats[1][2] + 10
             ]
    original = original[
               stats[1][1] - 10:stats[1][1] + stats[0][3] + 10,
               stats[1][0] - 10:stats[1][0] + stats[1][2] + 10
               ]

    return region, original, distances_from_boundary
