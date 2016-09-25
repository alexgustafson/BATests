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
import matplotlib.lines as mlines

#lesion_images = ProcessResult.objects.filter(evaluation__border_quality=10)
#lesion_images = ProcessResult.objects.filter(name="D239b.png") # example with border 0
#lesion_images = ProcessResult.objects.filter(name="C263a.png") # example with border 4
#lesion_images = ProcessResult.objects.filter(name="006027HB.jpeg") # example with border 8
#lesion_images = ProcessResult.objects.filter(source='PH2Dataset')
#lesion_images = ProcessResult.objects.filter(source='Dermofit').filter(evaluation__border_quality=10)


def segment_by_angle(number_of_segments, angle_array, data_array):

    cutoff_angle = int(360 / number_of_segments)

    segments = []
    start_index = 0
    start_angle = angle_array[0]

    for i in range(0, number_of_segments + 1):

        for j in range(start_index, len(data_array)):
            angle_diff = abs(start_angle - angle_array[j])
            if angle_diff > cutoff_angle:
                segments.append(data_array[start_index:j])
                start_index = j
                start_angle = angle_array[j]
                break

    if angle_diff < cutoff_angle:
        segments.append(data_array[start_index:j])

    return segments


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
            if '_lesion.bmp' in get_mask(lesion_image):
                border = array(Image.open(get_mask(lesion_image)).convert(mode='L'))
            else:
                border = array(Image.open(get_mask(lesion_image)))
        else:
            print(u'no mask found for {0}'.format(lesion_image))
            continue
    else:
        continue
    try:
        contour = calculate_contour(border)
    except:
        continue

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
    df_filtered_distance = array(distances) - distances[0]
    #hp_filtered_distances = butter_highpass_filter(df_filtered_distance, 20.0, 100.0)
    filtered_distances = gaussian_filter(df_filtered_distance, 5, 0)
    diff_dist = gradient(filtered_distances, 4)


    zerocross_dist_diff = []
    zerocross_angle_diff = []

    zero_cross_coords = []
    angle_signchange_coords = []

    for i in range(0, len(diff_dist)):
        if diff_dist[i-1] >= 0 and diff_dist[i] < 0:
            zerocross_dist_diff.append(1)
            zero_cross_coords.append(contour[i])
        elif diff_dist[i-1] <= 0 and diff_dist[i] > 0:
            zerocross_dist_diff.append(1)
            zero_cross_coords.append(contour[i])
        else:
            zerocross_dist_diff.append(0)

        if diff_angles[i] < 0 and diff_angles[i-1] >= 0:
            zerocross_angle_diff.append(1)
            angle_signchange_coords.append(contour[i])
        elif diff_angles[i] >= 0 and diff_angles[i - 1] < 0:
            zerocross_angle_diff.append(1)
            angle_signchange_coords.append(contour[i])
        else:
            zerocross_angle_diff.append(0)

    distance_scores = []
    for section in segment_by_angle(8, angles, zerocross_dist_diff):
        distance_scores.append(array(section).sum())

    angle_scores = []
    for section in segment_by_angle(8, angles, zerocross_angle_diff):
        angle_scores.append(array(section).sum())

    B_Score = 0
    point = 0
    for i in range(0, len(distance_scores)):
        point = 0
        if abs(distance_scores[i]) > 2.0:
            point = 1
        if angle_scores[i] > 0:
            point = 1
        B_Score += point

    print(B_Score)
    print(B_Score)

    lesion_image.border = B_Score
    lesion_image.save()
    #'''
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.imshow(border)

    for pixel in zero_cross_coords:
        dy = center[0] - pixel[0]
        dx = center[1] - pixel[1]
        ax.plot([center[1],pixel[1]], [center[0], pixel[0]], '-m')

    for pixel in angle_signchange_coords:
        dy = center[0] - pixel[0]
        dx = center[1] - pixel[1]
        ax.plot([center[1],pixel[1]], [center[0], pixel[0]], '-y')

    count = 1
    for section in segment_by_angle(8, angles, contour):

        dy = center[0] - section[0][0]
        dx = center[1] - section[0][1]
        text_distance = sqrt(dx * dx + dy * dy) * 1.1
        angle = atan2(dy, -dx)
        text_x = section[0][1] - (-cos(angle) * 20)
        text_y = section[0][0] - (sin(angle) * 20)


        ax.plot([center[1], section[0][1]], [center[0], section[0][0]], '-w')
        ax.text(text_x, text_y, u'{0}'.format(str(count)), fontsize=14, color='white')
        count += 1

    plt.tight_layout()
    show()

    m_line = mlines.Line2D([], [], color='magenta', label='distance function')
    g_line = mlines.Line2D([], [], color='green', label='filtered distance function')
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(311)
    ax.plot(X, df_filtered_distance, '-m')
    #ax.plot(X, hp_filtered_distances, '-r')
    ax.plot(X, filtered_distances, '-g')
    ax.legend(handles=[m_line, g_line])
    ax = fig.add_subplot(312)
    dm_line = mlines.Line2D([], [], color='magenta', label='filtered distance 1st derivative')
    ax.plot(X, diff_dist, '-m')
    ax.legend(handles=[dm_line])
    ax = fig.add_subplot(313)
    b_line = mlines.Line2D([], [], color='blue', label='difference of angles')
    ax.legend(handles=[b_line])
    ax.plot(X, diff_angles, '-b')

    show()

    #'''