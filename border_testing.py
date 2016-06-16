from utilities.images import imageDB
from utilities.border import find_border
from pylab import *
import matplotlib.pyplot as plt
from skimage.segmentation import mark_boundaries


#testing dermafit melanoma
source_images = imageDB.sources['Dermofit']['Categories']['Malignant Melanoma']

for src_image in source_images:
    fig = plt.figure(figsize=(12, 6))

    image = src_image.get_image_data()
    ax = fig.add_subplot(121)
    ax.imshow(image)
    ax.set_title('Original Image')


    border, mask, cropped, masked = find_border(image)

    ax = fig.add_subplot(122)
    ax.imshow(border)
    ax.set_title('Border')

    show()

