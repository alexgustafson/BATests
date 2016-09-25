from utilities.images import imageDB
from utilities.border import find_border
from pylab import *
import matplotlib.pyplot as plt
from skimage.segmentation import mark_boundaries
from os.path import join, abspath, dirname
import os



#testing dermafit melanoma
#source_images = imageDB.sources['PH2Dataset']['Categories']['Malignant Melanoma']
#source_images += imageDB.sources['PH2Dataset']['Categories']['Melanocytic Nevus']

#source_images += imageDB.sources['Dermofit']['Categories']['Melanocytic Nevus']
#source_images += imageDB.sources['Dermofit']['Categories']['Malignant Melanoma']
source_images = imageDB.sources['DermQuest']['Categories']['Malignant Melanoma']
#source_images = imageDB.sources['DermQuest']['Categories']['Melanocytic Nevus']
#source_images += imageDB.sources['DermQuest']['Categories']['Benign Keratosis']


this_path = os.path.dirname(os.path.realpath(__file__))
process_logs_path = join(this_path + '/logs/processlogs/')


for src_image in source_images:

    #fig = plt.figure(figsize=(12, 6))

    """ax = fig.add_subplot(121)
    ax.imshow(src_image.get_image_data())
    ax.set_title('Original Image')"""
    try:
        border, mask, cropped, masked = find_border(src_image, debug=True)
        src_image.save_process_log(join(process_logs_path))
    except:
        print("{0} failed processing".format(src_image.name))
        print(e)
        print("failed with image {0} from {1} - {2} : {3}".format(src_image.name, src_image.source, src_image.category, src_image.path))
        pass

    """ax = fig.add_subplot(122)
    ax.imshow(border)
    ax.set_title('Border')

    show()"""

