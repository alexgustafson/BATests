from utilities.images import imageDB
from utilities.border import find_border
from pylab import *
import matplotlib.pyplot as plt
from skimage.segmentation import mark_boundaries



#testing dermafit melanoma
source_images = imageDB.sources['DermQuest']['Categories']['Malignant Melanoma']
source_images += imageDB.sources['DermQuest']['Categories']['Melanocytic Nevus']
source_images += imageDB.sources['DermQuest']['Categories']['Benign Keratosis']
source_images += imageDB.sources['Dermofit']['Categories']['Melanocytic Nevus']
source_images += imageDB.sources['Dermofit']['Categories']['Malignant Melanoma']
source_images += imageDB.sources['PH2Dataset']['Categories']['Melanocytic Nevus']
source_images += imageDB.sources['PH2Dataset']['Categories']['Malignant Melanoma']

for src_image in source_images:

    #fig = plt.figure(figsize=(12, 6))

    """ax = fig.add_subplot(121)
    ax.imshow(src_image.get_image_data())
    ax.set_title('Original Image')"""
    try:
        border, mask, cropped, masked = find_border(src_image, debug=True)
    except:
        print("{0} failed processing".format(src_image.name))
        pass

    """ax = fig.add_subplot(122)
    ax.imshow(border)
    ax.set_title('Border')

    show()"""

