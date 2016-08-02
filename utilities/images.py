import os
from PIL import Image
from pylab import *
import csv
from path import path
from os.path import join

import json

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
        "exclude_contains": "_",
        "data_file": "PH2Dataset/PH2_dataset.txt",
    },

]


class ImageProcessResults():

    def __init__(self, shape):
        self.shape = shape
        self.size_index_threshold_log = []
        self.crop_to_center_log = []
        self.original_image = ""
        self.boundary_image = ""

    def log_index_threshold(self, size_index, threshold, center_region_touches_edge=False, path=""):
        self.size_index_threshold_log.append({
            'size_index': size_index,
            'threshold': threshold,
            'touches_edge': center_region_touches_edge,
            'image_path': path,
        })

    def log_crop_to_center(self, shape, segments, forecount):
        self.crop_to_center_log.append({
            'shape': shape,
            'segments': segments,
            'forecount': forecount.tolist(),
        })

    def set_boundary_image(self, image_path):
        self.boundary_image = image_path

    def set_original_image(self, image_path):
        self.original_image = image_path





class ImageItem():
    def __init__(self, source, path, mask=None, category=None, extra_data=None):
        self.source = source
        self.path = path
        self.mask = mask
        self.category = category
        self.name = path.split("/")[-1]
        self.extra_data = extra_data
        self.process_results = {}

    def get_image_data(self):
        if self.source == "DermQuest":
            # strip bottom copyright tag
            return array(Image.open(self.path))
        return array(Image.open(self.path))

    def __str__(self):
        return self.path

    def set_process_results(self, process_results):
        self.process_results = process_results

    def save_process_log(self, dirpath=os.path.dirname(os.path.realpath(__file__))):

        filename = "{0}.processlog.json".format(self.path.split('/')[-1])
        with open(join(dirpath + filename), 'w') as outfile:
            data = self.__dict__
            data['process_results'] = data['process_results'].__dict__
            json.dump(data, outfile, sort_keys=True,
                      indent=2, ensure_ascii=False)


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
                                mask = os.path.join(dirpath, filename)
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

            if source['name'] == "PH2Dataset":

                if not 'PH2Dataset' in self.sources:
                    self.sources['PH2Dataset'] = {}
                    self.sources['PH2Dataset']['Images'] = []
                    self.sources['PH2Dataset']['Categories'] = {}

                with open(path(source["data_file"])) as csvfile:
                    spamreader = csv.DictReader(csvfile, delimiter='|')
                    for row in spamreader:

                        if row.get('   Name ', False):
                            ph2Data = PH2Data(row)
                            image_file = 'PH2Dataset/PH2 Dataset images/{0}/{0}_Dermoscopic_Image/{0}.bmp'.format(ph2Data.name)
                            mask_file = 'PH2Dataset/PH2 Dataset images/{0}/{0}_lesion/{0}_lesion.bmp'.format(ph2Data.name)

                            image = ImageItem('PH2Dataset', image_file, mask_file, extra_data=ph2Data.__dict__)

                            if ph2Data.clinical_diagnosis == '0':

                                image.category = "Melanocytic Nevus"

                            elif ph2Data.clinical_diagnosis == '1':

                                image.category = "Melanocytic Nevus"

                            else:

                                image.category = "Malignant Melanoma"

                            if not image.category in self.categories:
                                self.categories[image.category] = []
                            if not image.category in self.sources['PH2Dataset']['Categories']:
                                self.sources['PH2Dataset']['Categories'][image.category] = []

                            self.categories[image.category].append(image)
                            self.sources['PH2Dataset']['Categories'][image.category].append(image)
                            self.sources['PH2Dataset']['Images'].append(image)
                            self.images.append(image)


# gather all images in all_image_root and store them in all_images
class PH2Data():

    name = ''

    def __init__(self, data):

        self.name = data.get('   Name ', '').strip()
        self.colors = data.get('           Colors ', '').strip().split(' ')
        self.asymmetry = data.get(' Asymmetry ', '').strip()
        self.blue_whitish_veil = data.get(' Blue-Whitish Veil ', '').strip()
        self.clinical_diagnosis = data.get(' Clinical Diagnosis ', '').strip()
        self.dots_globules = data.get(' Dots/Globules ', '').strip()
        self.histological_diagnosis = data.get(' Histological Diagnosis ', '').strip()
        self.pigment_network = data.get(' Pigment Network ', '').strip()
        self.regression_areas = data.get(' Regression Areas ', '').strip()
        self.streaks = data.get(' Streaks ', '').strip()



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

