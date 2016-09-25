from utilities.images import all_images, imageDB
from utilities.border import find_border
from utilities.radii import calculate_radii
from utilities.sfa import sfa
from pylab import *
import matplotlib.pyplot as plt
from skimage.segmentation import mark_boundaries
from skimage import color
from skimage import measure
import cv2

images = imageDB.sources["Dermofit"]['Categories']['Malignant Melanoma']

for im in images:
    try:
        border, mask, cropped, masked = find_border(im)
    except:
        print('could not create masks')
        pass

fig = plt.figure(figsize=(19, 19))
ax = fig.add_subplot(111)
blank = np.zeros((cropped.shape[0],cropped.shape[1]))
boundary = color.rgb2grey(mark_boundaries(blank, border))
ax.imshow(boundary,cmap='Greys_r' )

radii = calculate_radii(border)
main_axis, minor_axis = sfa(radii)

print('## major symetrie : ')
print('max angle : %s' % main_axis['angle'])
print('SFAa score : %s' % main_axis['SFAa'])

print('## minor symetrie : ')
print('theta angle : %s' % minor_axis['angle'])
print('SFAa score : %s' % minor_axis['SFAa'])

props = measure.regionprops(border)[0]
center = props.centroid

ax.plot([center[1], radii[15]['point'][0]], [center[0], radii[15]['point'][1]], '-y')
ax.plot([center[1], radii[50]['point'][0]], [center[0], radii[50]['point'][1]], '-g')
ax.plot([center[1], radii[-20]['point'][0]], [center[0], radii[-20]['point'][1]], '-g')

#ax.plot([center[1], main_axis['point'][0]], [center[0], main_axis['point'][1]], '-r')

#ax.plot([center[1], minor_axis['point'][0]], [center[0], minor_axis['point'][1]], '-b')

show()
