import matplotlib.pyplot as plt
import utilities.start_django
from border_results.models import ProcessResult
from pylab import *
from sklearn import datasets
from sklearn import svm


digits = datasets.load_digits()

for digit in digits:
    pass


lesion_images_m = ProcessResult.objects.filter(source='Dermofit').filter(evaluation__border_quality=10).filter(category='Malignant Melanoma').order_by('?')
lesion_images_n = ProcessResult.objects.filter(source='Dermofit').filter(evaluation__border_quality=10).filter(category='Melanocytic Nevus').order_by('?')

min_count = min(len(lesion_images_m), len(lesion_images_n))
half_min = int(min_count / 2)

train_m = lesion_images_m[:half_min]
train_n = lesion_images_n[:half_min]

test_m = lesion_images_m[half_min:]
test_n = lesion_images_n[half_min:]

train_set = [item for item in train_m] + [item for item in train_n]
test_set = [item for item in test_m] + [item for item in test_n]


def prepare_data(image):
    data_item = [float(image.SFA_major/360), float(image.SFA_minor/360), float(image.border), image.black, image.blue_gray, image.red, image.white, image.light_brown, image.dark_brown ]

    if image.SFA_major > 140 and image.SFA_minor > 140:
        image.asymmetry = 0
    elif image.SFA_major > 140 and image.SFA_minor <= 140:
        image.asymmetry = 1
    else:
        image.asymmetry = 2

    image.tds = image.asymmetry * 1.3
    image.tds += image.border * 0.1
    image.tds += image.color_score * 0.5

    target_item = 0

    if image.category == 'Malignant Melanoma':
        target_item = 1

    return np.array(data_item), target_item


data = []
target = []

for i in range(0, len(train_set) - 1):

    x, y = prepare_data(train_set[i])
    data.append(x)
    target.append(y)

data = array(data)
target = array(target)

#clf = svm.SVC(gamma=0.001, C=100)
clf = svm.SVC()
clf.fit(data, target)



for j in range(0, len(test_set)-1):
    data, targe = prepare_data(test_set[j])
    print(u'Predicted: {0}, Is {1}'.format(clf.predict([data]), test_set[j].category))