from PIL import Image
import utilities.start_django
from border_results.models import ProcessResult
from utilities.radii import calculate_radii
from utilities.sfa import sfa
from pylab import *
import os.path


#lesion_images = ProcessResult.objects.all()
lesion_images = ProcessResult.objects.filter(source='PH2Dataset')


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
    try:
        radii = calculate_radii(border)
        main_axis, minor_axis = sfa(radii)

        lesion_image.major_axis_angle = main_axis['angle']
        lesion_image.SFA_major = main_axis['SFAa']
        lesion_image.SFA_minor = minor_axis['SFAa']
        lesion_image.save()
    except:
        pass