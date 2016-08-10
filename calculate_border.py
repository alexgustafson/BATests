from PIL import Image
import utilities.start_django
from border_results.models import ProcessResult
from utilities.contour import calculate_contour
from pylab import *
import os.path
from skimage import measure
from math import atan2, degrees, sqrt
import cv2
from skimage import img_as_uint
from scipy.signal import savgol_filter, butter, lfilter
from scipy.ndimage.filters import gaussian_filter

lesion_images = ProcessResult.objects.all()

def butter_highpass(cutOff, fs, order=5):
    nyq = 0.5 * fs
    normalCutoff = cutOff / nyq
    b, a = butter(order, normalCutoff, btype='high', analog = True)
    return b, a


def butter_highpass_filter(data, cutOff, fs, order=4):
    b, a = butter_highpass(cutOff, fs, order=order)
    y = lfilter(b, a, data)
    return y


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
            border = array(Image.open(get_mask(lesion_image)))
        else:
            print(u'no mask found for {0}'.format(lesion_image))
            continue
    else:
        continue

    contour = calculate_contour(border)

    if len(border.shape) == 2:
        if border[0][0] == False:
            border = img_as_uint(border)
        else:

            ret, border = cv2.threshold(border, 2, 255, cv2.THRESH_BINARY)
    else:
        ret, border = cv2.threshold(border[:, :, 0], 2, 255, cv2.THRESH_BINARY)

    props = measure.regionprops(border)

    if len(props) > 1:
        raise Exception('Too many regions detected. Border should be a binary mask of a single region.')

    props = props[0]
    radii = []
    center = props.centroid  # verified is equal to center of mass

    dx = 0
    dy = 0

    contour_properties = []
    i = 0
    X = []
    sum_distance = 0
    distances = []
    angles = []
    previous_angle = 90

    for pixel in contour:
        dy = center[0] - pixel[0]
        dx = center[1] - pixel[1]
        distance = sqrt(dx * dx + dy * dy)
        angle = degrees(atan2(dy, -dx))

        if abs(previous_angle - angle) > 350:
            angle -= 360

        contour_properties.append({
            'coordinate': pixel,
            'distance': distance,
            'angle': angle,
        })
        X.append(i)
        distances.append(distance)
        angles.append(angle)
        previous_angle = angle
        i += 1
        sum_distance += distance


    diff_angles = []
    previous_angle = False
    for angle in angles:
        if previous_angle:
            diff_angles.append(previous_angle - angle)
        else:
            diff_angles.append((angles[-1] + 360) - angle)

        previous_angle = angle


    avg = sum_distance / i
    df_filtered_distance = [x - avg for x in distances]
    hp_filtered_distances = butter_highpass_filter(df_filtered_distance, 40.0, 100.0)
    filtered_distances = gaussian_filter(hp_filtered_distances, 8, 0)
    diff_dist = gradient(filtered_distances, 4)


    zerocross_dist_diff = []
    zerocross_angle_diff = []

    for i in range(0, len(diff_dist)):
        if diff_dist[i-1] >= 0 and diff_dist[i] < 0:
            zerocross_dist_diff.append( abs(filtered_distances[i]))
        elif diff_dist[i-1] <= 0 and diff_dist[i] > 0:
            zerocross_dist_diff.append(abs(filtered_distances[i]))
        else:
            zerocross_dist_diff.append(0)

        if diff_angles[i] < 0:
            zerocross_angle_diff.append(1)
        else:
            zerocross_angle_diff.append(0)

    distance_scores = []
    for section in array_split(array(zerocross_dist_diff), 8):
        distance_scores.append(section.sum())

    angle_scores = []
    for section in array_split(array(zerocross_angle_diff), 8):
        angle_scores.append(section.sum())

    B_Score = 0
    point = 0
    for i in range(0, 8):
        point = 0
        if abs(distance_scores[i]) > 1.0:
            point = 1
        if angle_scores[i] > 0:
            point = 1
        B_Score += point

    print(B_Score)

    lesion_image.border = B_Score
    lesion_image.save()
    '''
    fig = plt.figure(figsize=(8, 14))
    ax = fig.add_subplot(311)
    ax.imshow(border)
    ax = fig.add_subplot(312)

    ax.plot(X, df_filtered_distance, '-b')
    ax.plot(X, hp_filtered_distances, '-r')
    ax.plot(X, filtered_distances, '-g')
    ax = fig.add_subplot(313)
    ax.plot(X, diff_angles, '-b')

    show()
    '''
