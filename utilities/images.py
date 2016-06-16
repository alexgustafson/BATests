import os
from PIL import Image
from pylab import *

all_images = {}
image_roots = [
    {
        "name": "DermQuest",
        "path": "DermQuest/",
        "exclude_contains": [".DS_Store",],
        "categories": [{
            'name': 'Melanocytic Nevus',
            'path': "DysplasticNevus",
        }, {
            'name': 'Melanocytic Nevus',
            'path': "IntradermalNevus",
        }, {
            'name': 'Melanocytic Nevus',
            'path': "CompoundNevus",
        }, {
            'name': 'Malignant Melanoma',
            'path': "MalignantMelanoma",
        }, {
            'name': 'Benign Keratosis',
            'path': "BenignKeratosis",
        }],
    },
    {
        "name": "Dermofit",
        "path": "Dermofit/",
        "has_masks": True,
        "include_endswith": ".png",
        "exclude_contains": "mask",
        "mask_contains": "mask",
        "categories": [{
            'name': 'Actinic Keratosis',
            'path': "Actinic Keratosis Images",
        }, {
            'name': 'Basal Cell Carcinoma',
            'path': "Basal Cell Carcinoma Images",
        }, {
            'name': 'Dermatofibroma',
            'path': "Dermatofibroma Images",
        }, {
            'name': 'Haemangioma',
            'path': "Haemangioma Images",
        }, {
            'name': 'Intraepithelial Carcinoma',
            'path': "Intraepithelial Carcinoma Images",
        }, {
            'name': 'Malignant Melanoma',
            'path': "Malignant Melanoma Images",
        }, {
            'name': 'Melanocytic Nevus',
            'path': "Melanocytic Nevus (mole) Images",
        }, {
            'name': 'Pyogenic Granuloma',
            'path': "Pyogenic Granuloma Images",
        }, {
            'name': 'Seborrhoeic Keratosis',
            'path': "Seborrhoeic Keratosis Images",
        }, {
            'name': 'Squamous Cell Carcinoma',
            'path': "Squamous Cell Carcinoma Images",
        }],
    },
    {
        "name": "PH2Dataset",
        "path": "PH2Dataset/PH2 Dataset images",
        "include_endswith": ".bmp",
        "exclude_contains": "_"},
]


class ImageItem():
    def __init__(self, source, path, mask=None, category=None):
        self.source = source
        self.path = path
        self.mask = mask
        self.category = category

    def get_image_data(self):
        if self.source == "DermQuest":
            # strip bottom copyright tag
            return array(Image.open(self.path))
        return array(Image.open(self.path))

    def __str__(self):
        return self.path


class Images():
    def __init__(self, image_data):
        self.categories = {}
        self.images = []
        self.sources = {}
        self.paths = {}

        for source in image_data:

            if source['name'] == "Dermofit":

                if not 'Dermofit' in self.sources:
                    self.sources['Dermofit'] = {}
                    self.sources['Dermofit']['Images'] = []
                    self.sources['Dermofit']['Categories'] = {}

                for dirpath, dirnames, filenames in os.walk(source["path"]):
                    image = None
                    mask = None

                    for filename in filenames:

                        if filename.endswith(source["include_endswith"]):

                            if source["mask_contains"] in filename:
                                mask = ImageItem(
                                            path=os.path.join(dirpath, filename),
                                            source=source['name']
                                        )
                            else:
                                image = ImageItem(
                                    path=os.path.join(dirpath, filename),
                                    source=source['name']
                                )

                    if mask:
                        image.mask = mask

                    if image:

                        self.images.append(image)

                        for category in source['categories']:
                            category_name = category['name']

                            if category['path'] in image.path:
                                if not category_name in self.categories:
                                    self.categories[category_name] = []
                                if not category_name in self.sources['Dermofit']['Categories']:
                                    self.sources['Dermofit']['Categories'][category_name] = []

                                self.categories[category_name].append(image)
                                self.sources['Dermofit']['Categories'][category_name].append(image)
                                image.category = category_name

            if source['name'] == "DermQuest":

                if not 'DermQuest' in self.sources:
                    self.sources['DermQuest'] = {}
                    self.sources['DermQuest']['Images'] = []
                    self.sources['DermQuest']['Categories'] = {}

                for dirpath, dirnames, filenames in os.walk(source["path"]):

                    for filename in filenames:
                        image = None
                        exclude = False
                        for exclude_term in source['exclude_contains']:
                            if exclude_term in filename:
                                exclude = True
                        if exclude:
                            continue

                        image = ImageItem(
                                    path=os.path.join(dirpath, filename),
                                    source=source['name']
                                )

                        if image:

                            self.images.append(image)

                            for category in source['categories']:
                                category_name = category['name']

                                if category['path'] in image.path:
                                    if not category_name in self.categories:
                                        self.categories[category_name] = []
                                    if not category_name in self.sources['DermQuest']['Categories']:
                                        self.sources['DermQuest']['Categories'][category_name] = []

                                    self.categories[category_name].append(image)
                                    self.sources['DermQuest']['Categories'][category_name].append(image)
                                    image.category = category_name



# gather all images in all_image_root and store them in all_images


def gather_images():
    images = {}
    for root in image_roots:

        root_list = []

        if "include_endswith" in root and "exclude_contains" in root:
            for dirpath, dirnames, filenames in os.walk(root["path"]):
                for filename in [f for f in filenames if
                                 (f.endswith(root["include_endswith"]) and root["exclude_contains"] not in f)]:
                    root_list.append(
                        ImageItem(
                            path=os.path.join(dirpath, filename),
                            source=root['name']
                        )
                    )
        else:
            for dirpath, dirnames, filenames in os.walk(root["path"]):
                for filename in [f for f in filenames]:
                    root_list.append(
                        ImageItem(
                            path=os.path.join(dirpath, filename),
                            source=root['name']
                        )
                    )
        images[root["name"]] = root_list
    return images


imageDB = Images(image_roots)
all_images = gather_images()

