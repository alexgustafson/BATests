from skimage.segmentation import mark_boundaries
from skimage import color
from pylab import *


def pixel_equals_pixel(pixA, pixB):
    if pixA[0] == pixB[0] and pixA[1] == pixB[1]:
        return True
    return False


def not_in_contour_pixels(pixel, array_of_pixels):
    for i in range(0, len(array_of_pixels)):
        test_pixel = array_of_pixels[i]
        if pixel_equals_pixel(test_pixel, pixel):
            return False
    return True


def calculate_contour(border):

    blank = np.zeros((border.shape[0], border.shape[1]))
    if len(border.shape) > 2:
        boundary = color.rgb2grey(mark_boundaries(blank, border[:,:,0]))
    else:
        boundary = color.rgb2grey(mark_boundaries(blank, border))


    contour_pixels = []
    pix_v = 0.0
    x = -1
    y = -1

    # choose a start pixel
    for i in range(0, boundary.shape[0]):
        for j in range(0, boundary.shape[1]):

            pix_v = boundary[i,j]
            if pix_v > 0:
                break
        if pix_v > 0:
            break

    start_pixel = [i,j]
    range_center = start_pixel

    range_distance = 1
    last_pixel = start_pixel
    next_pixel = start_pixel
    found = False

    for i in range(-range_distance, range_distance+1):
        for j in range(-range_distance, range_distance+1):
            if i == 0 and j == 0:
                continue
            if boundary[start_pixel[0]+i, start_pixel[1]+j] == 0.0:
                continue
            next_pixel = [start_pixel[0]+i, start_pixel[1]+j]
            found = True
            break
        if found:
            break

    contour_pixels.append(start_pixel)
    contour_pixels.append(next_pixel)

    last_pixel = next_pixel

    while not pixel_equals_pixel(start_pixel,next_pixel):
        found = False

        section = boundary[last_pixel[0]-range_distance:last_pixel[0]+range_distance+1, last_pixel[1]-range_distance:last_pixel[1]+range_distance+1]

        for i in range(-range_distance, range_distance+1):
            for j in range(range_distance, -(range_distance + 1), -1):
                if abs(i) < range_distance and abs(j) < range_distance:
                    continue
                if abs(last_pixel[0] + i) < boundary.shape[0] and abs(last_pixel[1] + j) < boundary.shape[1]:
                    if boundary[last_pixel[0] + i, last_pixel[1] + j] == 0.0:
                        continue
                else:
                    continue
                test_pixel = [last_pixel[0] + i, last_pixel[1] + j]

                if pixel_equals_pixel(test_pixel, start_pixel) and len(contour_pixels) > 10:
                    next_pixel = test_pixel
                    found = True
                    break

                if not_in_contour_pixels(test_pixel, contour_pixels):
                    next_pixel = test_pixel
                    found = True
                    contour_pixels.append(next_pixel)
                    break
                next_pixel = test_pixel
            if found:

                break
        if found:
            range_distance = 1
            last_pixel = next_pixel
        else:
            range_distance += 1
            if range_distance > boundary.shape[0] and range_distance > boundary.shape[1]:
                return contour_pixels


    X = []
    Y = []
    for i in range(0, len(contour_pixels)):
        X.append(contour_pixels[i][1])
        Y.append(contour_pixels[i][0])


    return contour_pixels
