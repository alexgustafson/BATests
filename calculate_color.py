from PIL import Image
import utilities.start_django
from border_results.models import ProcessResult
from utilities.region_of_interest import get_region
from pylab import *
import os.path
from scipy.signal import butter, lfilter
from scipy.spatial.distance import euclidean
from cv2 import GaussianBlur

#lesion_images = ProcessResult.objects.filter(evaluation__border_quality=10)
#lesion_images = ProcessResult.objects.filter(name="IMD430.bmp")
#lesion_images = ProcessResult.objects.filter(name="019682HB.JPG")
#lesion_images = ProcessResult.objects.filter(name="020250HB.JPG")
#lesion_images = ProcessResult.objects.filter(name="020069HB.JPG")
#lesion_images = ProcessResult.objects.filter(name="B522b.png")  # example color = 1
#lesion_images = ProcessResult.objects.filter(name="020319HB.JPG")  # example color = 5
lesion_images = ProcessResult.objects.filter(name="020302HB.JPG")  # example color = 4
#lesion_images = ProcessResult.objects.filter(name="B65.png")  # example color = 3
#lesion_images = ProcessResult.objects.filter(name="019523HB.JPG")  # example color = 6
#lesion_images = ProcessResult.objects.filter(source='PH2Dataset')
#lesion_images = ProcessResult.objects.filter(source='Dermofit').filter(evaluation__border_quality=10)


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


for lesion_image in lesion_images:

    print(lesion_image)
    if lesion_image.name == 'B102d.png':
        print('debug')

    if result_has_mask(lesion_image):
        if os.path.exists(get_mask(lesion_image)):
            if '_lesion.bmp' in get_mask(lesion_image):
                mask = array(Image.open(get_mask(lesion_image)).convert(mode='L'))
            else:
                mask = array(Image.open(get_mask(lesion_image)))
        else:
            print(u'no mask found for {0}'.format(lesion_image))
            continue
    else:
        continue
    mask_shape = ','.join(str(i) for i in mask.shape[0:2])
    lesion_shape = ','.join(str(i) for i in lesion_image.shape.split(',')[0:2])
    try:
        if not mask_shape == lesion_shape:
            path = lesion_image.calculated_mask
            path = path.replace('.E_border.', '.D_cropped.')
            image = GaussianBlur(array(Image.open(path)), (5, 5), 0)
            region_of_interest = get_region(image, mask)
        else:
            image = GaussianBlur(array(Image.open(lesion_image.path)), (5, 5), 0)
            region_of_interest = get_region(image, mask)
    except:
        continue


    color_white = array([255, 255, 255])
    color_red = array([204, 51, 51])
    color_light_brown = array([153, 102, 0])
    color_dark_brown = array([51, 0, 0])
    color_blue_gray = array([51, 153, 255])
    color_black = array([0, 0, 0])

    select_colors = [color_white, color_red, color_light_brown, color_dark_brown, color_blue_gray, color_black]

    colors = array([0, 0, 0, 0, 0, 0])
    color_count = array([0., 0., 0., 0., 0., 0.])

    image_copy = copy(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):

            pixel = image[i][j]
            mask_pixel = mask[i][j]

            if isinstance(mask_pixel, (list, tuple, np.ndarray)):
                mask_value = mask_pixel[0]
            else:
                mask_value = mask_pixel

            if mask_value > 0:
                colors[0] = euclidean(color_white, pixel[0:3])
                colors[1] = euclidean(color_red, pixel[0:3])
                colors[2] = euclidean(color_light_brown, pixel[0:3])
                colors[3] = euclidean(color_dark_brown, pixel[0:3])
                colors[4] = euclidean(color_blue_gray, pixel[0:3])
                colors[5] = euclidean(color_black, pixel[0:3])

                closest = min(colors)
                not_near_indicies = colors > closest
                closest_indicies = colors == closest
                colors[not_near_indicies] = 0.
                colors[closest_indicies] = 1.

                color_count += colors

                for k in range(0, len(colors)):
                    if colors[k] == 1:
                        image_copy[i][j][0:3] = select_colors[k]
                        continue

            else:
                image_copy[i][j][0:3] = [0, 0, 255]



    pixel_total = sum(color_count)
    color_count /= pixel_total

    lesion_image.white = color_count[0]
    lesion_image.red = color_count[1]
    lesion_image.light_brown = color_count[2]
    lesion_image.dark_brown = color_count[3]
    lesion_image.blue_gray = color_count[4]
    lesion_image.black = color_count[5]

    threshold_indexes = color_count < 0.01
    color_count[threshold_indexes] = 0.

    threshold_indexes = color_count >= 0.01
    color_count[threshold_indexes] = 1.

    color_score = sum(color_count)

    lesion_image.color_score = color_score
    lesion_image.save()

    #'''
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(121)
    ax.imshow(image)
    ax = fig.add_subplot(122)
    ax.imshow(image_copy)

    print(color_score)

    show()
    #'''

