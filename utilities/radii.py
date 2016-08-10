from skimage import measure
from math import atan2, degrees, sqrt
import cv2
from skimage import img_as_ubyte, img_as_uint

def calculate_radii(border):
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

    for i in range(0, 90):
        value = 100
        dx = 0;
        dy = 0;
        while value > 0.0 and dx < center[1] and dy < center[0]:

            if degrees(atan2(dy, dx)) > i:
                dx += 1
            else:
                dy += 1

            value = border[center[0] - dy, center[1] + dx]
            distance = sqrt(dx * dx + dy * dy)

        radii.append({'distance': distance, 'angle': i, 'point': (center[1] + dx, center[0] - dy)})

    for i in range(90, 180):
        value = 100
        dx = 0;
        dy = 0;
        while value > 0.0 and dx < center[1] and dy < center[0]:

            if degrees(atan2(dy, -dx)) < i:
                dx += 1
            else:
                dy += 1

            value = border[center[0] - dy, center[1] - dx]
            distance = sqrt(dx * dx + dy * dy)

        radii.append({'distance': distance, 'angle': i, 'point': (center[1] - dx, center[0] - dy)})

    for i in range(180, 270):
        value = 100
        dx = 0;
        dy = 0;
        while value > 0.0 and dx < center[1] and dy < center[0]:
            angle = 180 + degrees(atan2(dy, dx))
            if angle > i:
                dx += 1
            else:
                dy += 1

            value = border[center[0] + dy, center[1] - dx]
            distance = sqrt(dx * dx + dy * dy)

        radii.append({'distance': distance, 'angle': i, 'point': (center[1] - dx, center[0] + dy)})

    for i in range(270, 360):
        value = 100
        dx = 0;
        dy = 0;
        while value > 0.0 and dx < center[1] and dy < center[0]:
            value = border[center[0] + dy, center[1] + dx]
            distance = sqrt(dx * dx + dy * dy)
            angle = 180 + degrees(atan2(dy, -dx))
            if angle < i:
                dx += 1
            else:
                dy += 1

        radii.append({'distance': distance, 'angle': i, 'point': (center[1] + dx, center[0] + dy)})

    return radii
