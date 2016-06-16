from utilities.images import all_images, imageDB
from utilities.border import find_border
from pylab import *
import matplotlib.pyplot as plt
from skimage.segmentation import mark_boundaries

im = all_images["Dermofit"][537].get_image_data()
border, mask, cropped, masked = find_border(im)

from skimage import measure
from skimage import transform
from scipy.ndimage.measurements import center_of_mass
from skimage import img_as_uint

props = measure.regionprops(border)

# get center of gravity
center = center_of_mass(border)

rotated = transform.rotate(img_as_uint(border), - (props[0].orientation/pi)*180, resize=True, center=center, mode='edge')
props = measure.regionprops(img_as_uint(rotated))
bbox = props[0].bbox
rotated = rotated[bbox[0]:bbox[2], bbox[1]:bbox[3]]

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111)

blank = np.zeros((rotated.shape[0],rotated.shape[1]))
boundary = mark_boundaries(blank, img_as_uint(rotated))

props = measure.regionprops(img_as_uint(rotated))
center = props[0].centroid

from math import atan2, degrees, sqrt

ax.imshow(rotated)
ranges = []

center = (int(rotated.shape[0]/2), int(rotated.shape[1]/2))

for i in range(90):
    value = 100
    dx = 0;
    dy = 0;
    while value > 0.0 and dx < center[1] and dy < center[0]:

        if degrees(atan2(dy, dx)) > i:
            dx += 1
        else:
            dy += 1

        value = rotated[center[0]-dy,center[1]+dx]
        distance = sqrt(dx*dx + dy*dy)

    ranges.append({'distance':distance, 'angle': i, 'point': (center[1]+dx, center[0]-dy)})
    ax.plot((center[1], center[1]+dx), (center[0], center[0] - dy), '-r', linewidth=0.5)


for i in range(90, 180):
    value = 100
    dx = 0;
    dy = 0;
    while value > 0.0 and dx < center[1] and dy < center[0]:

        if degrees(atan2(dy, -dx)) < i:
            dx += 1
        else:
            dy += 1

        value = rotated[center[0]-dy,center[1]-dx]
        distance = sqrt(dx*dx + dy*dy)

    ranges.append({'distance':distance, 'angle': i, 'point': (center[0]-dx, center[0]-dy)})
    ax.plot((center[1], center[1] - dx), (center[0], center[0] - dy), '-r', linewidth=0.5)


for i in range(181, 270):
    value = 100
    dx = 0;
    dy = 0;
    while value > 0.0 and dx < center[1] and dy < center[0]:
        angle = 180 + degrees( atan2(dy, dx))
        if angle > i:
            dx += 1
        else:
            dy += 1

        value = rotated[center[0]+dy,center[1]-dx]
        distance = sqrt(dx*dx + dy*dy)

    ranges.append({'distance':distance, 'angle': i, 'point': (center[0]-dx, center[0]+dy)})
    ax.plot((center[1], center[1] - dx), (center[0], center[0] + dy), '-r', linewidth=0.5)

for i in range(271, 360):
    value = 100
    dx = 0;
    dy = 0;
    while value > 0.0 and dx < center[1] and dy < center[0]:
        value = rotated[center[0] + dy, center[1] + dx]
        distance = sqrt(dx * dx + dy * dy)
        angle = 180 + degrees( atan2(dy, -dx))
        if angle < i:
            dx += 1
        else:
            dy += 1

    ranges.append({'distance':distance, 'angle': i, 'point': (center[0]+dx, center[0]+dy)})
    ax.plot((center[1], center[1] + dx), (center[0], center[0] + dy), '-r', linewidth=0.5)


show()
