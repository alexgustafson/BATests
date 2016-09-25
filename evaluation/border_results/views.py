from django.shortcuts import render
from os import listdir
from os.path import isfile, join
import json
from django.http import JsonResponse
from .models import ProcessResult
from django.core import serializers



def initialize(request):

    results_path = join('../', 'logs/processlogs/')
    all_files = [f for f in listdir(results_path) if isfile(join(results_path, f)) and f != '.DS_Store']

    for file in all_files:
        file_path = join('../', 'logs/processlogs/', file)
        json_data = open(file_path)
        try:
            data2 = json.load(json_data)
            process_result, created = ProcessResult.objects.get_or_create(name=data2['name'], source=data2['source'])
            process_result.setDataFromJson(data2, file)
        except:
            print(file_path)

        pass

    return render(request, 'border_results/result.jade', {})


def index(request):

    results_path = join('../', 'logs/processlogs/')
    all_files = [f for f in listdir(results_path) if isfile(join(results_path, f)) and f != '.DS_Store']

    return render(request, 'border_results/list.jade', {'files': all_files})


def processlogs(request):

    if request.method == 'GET':

        data = request.GET

        if 'filename' in data:

            file_path = join('../', 'logs/processlogs/', data['filename'])

            json_data = open(file_path)
            data2 = json.load(json_data)

            result = ProcessResult.objects.get(json_file=data['filename'])
            result = serializers.serialize('json', result)

            return JsonResponse(result, safe=False)

        else:

            results_path = join('../', 'logs/processlogs/')
            all_files = [f for f in listdir(results_path) if isfile(join(results_path, f)) and f != '.DS_Store']

            return JsonResponse({'files': all_files})

    return render(request, 'border_results/list.jade', {'files': ['fa', 'ma']})


def results(request):
    Dermofit = ProcessResult.objects.filter(evaluation__border_quality=10).filter(source='Dermofit').order_by('category')
    Dermquest = ProcessResult.objects.filter(evaluation__border_quality=10).filter(source='DermQuest').order_by('category')
    PH2 = ProcessResult.objects.filter(evaluation__border_quality=10).filter(source='PH2Dataset').order_by('category')

    for lesion in Dermofit:
        if lesion.SFA_major > 140 and lesion.SFA_minor > 140:
            lesion.asymmetry = 0
        elif lesion.SFA_major > 140 and lesion.SFA_minor <= 140:
            lesion.asymmetry = 1
        else:
            lesion.asymmetry = 2

        lesion.tds = lesion.asymmetry * 1.3
        lesion.tds += lesion.border * 0.1
        lesion.tds += lesion.color_score * 0.5

        lesion.tds = format(lesion.tds, '.2f')

    for lesion in Dermquest:
        if lesion.SFA_major > 140 and lesion.SFA_minor > 140:
            lesion.asymmetry = 0
        elif lesion.SFA_major > 140 and lesion.SFA_minor <= 140:
            lesion.asymmetry = 1
        else:
            lesion.asymmetry = 2

        lesion.tds = lesion.asymmetry * 1.3
        lesion.tds += lesion.border * 0.1
        lesion.tds += lesion.color_score * 0.5

        lesion.tds = format(lesion.tds, '.2f')

    for lesion in PH2:
        if lesion.SFA_major > 140 and lesion.SFA_minor > 140:
            lesion.asymmetry = 0
        elif lesion.SFA_major > 140 and lesion.SFA_minor <= 140:
            lesion.asymmetry = 1
        else:
            lesion.asymmetry = 2

        lesion.tds = lesion.asymmetry * 1.3
        lesion.tds += lesion.border * 0.1
        lesion.tds += lesion.color_score * 0.5

        lesion.tds = format(lesion.tds, '.2f')

    return render(request, 'border_results/table.jade', {'Dermofit': Dermofit, 'Dermquest': Dermquest, 'PH2': PH2})


class ResultItem:

    def __init__(self, source):
        self.source = source
        self.false_positives = 0
        self.false_negatives = 0
        self.correct = 0
        self.total_malignant = 0
        self.total_malignant_correct = 0
        self.total = 0


def evaluation(request):
    Dermofit = ProcessResult.objects.filter(evaluation__border_quality=10).filter(source='Dermofit').order_by('category')
    Dermquest = ProcessResult.objects.filter(evaluation__border_quality=10).filter(source='DermQuest').order_by('category')
    PH2 = ProcessResult.objects.filter(evaluation__border_quality=10).filter(source='PH2Dataset').order_by('category')

    Results = []
    result = ResultItem('Dermofit')

    for lesion in Dermofit:
        if lesion.SFA_major > 140 and lesion.SFA_minor > 140:
            lesion.asymmetry = 0
        elif lesion.SFA_major > 140 and lesion.SFA_minor <= 140:
            lesion.asymmetry = 1
        else:
            lesion.asymmetry = 2

        lesion.tds = lesion.asymmetry * 1.3
        lesion.tds += lesion.border * 0.1
        lesion.tds += lesion.color_score * 0.5

        if lesion.category == 'Malignant Melanoma':
            result.total_malignant += 1

        if lesion.tds < 3.2 and lesion.category == 'Malignant Melanoma':
            result.false_negatives += 1
        elif lesion.tds > 3.7 and lesion.category != 'Malignant Melanoma':
            result.false_positives += 1
        else:
            result.correct += 1
            if lesion.category == 'Malignant Melanoma':
                result.total_malignant_correct += 1

        result.total += 1

    Results.append(result)
    result = ResultItem('Dermquest')

    for lesion in Dermquest:
        if lesion.SFA_major > 140 and lesion.SFA_minor > 140:
            lesion.asymmetry = 0
        elif lesion.SFA_major > 140 and lesion.SFA_minor <= 140:
            lesion.asymmetry = 1
        else:
            lesion.asymmetry = 2

        lesion.tds = lesion.asymmetry * 1.3
        lesion.tds += lesion.border * 0.1
        lesion.tds += lesion.color_score * 0.5

        if lesion.category == 'Malignant Melanoma':
            result.total_malignant += 1

        if lesion.tds < 3.2 and lesion.category == 'Malignant Melanoma':
            result.false_negatives += 1
        elif lesion.tds > 3.7 and lesion.category != 'Malignant Melanoma':
            result.false_positives += 1
        else:
            result.correct += 1
            if lesion.category == 'Malignant Melanoma':
                result.total_malignant_correct += 1

        result.total += 1

    Results.append(result)
    result = ResultItem('PH2')


    for lesion in PH2:
        if lesion.SFA_major > 140 and lesion.SFA_minor > 140:
            lesion.asymmetry = 0
        elif lesion.SFA_major > 140 and lesion.SFA_minor <= 140:
            lesion.asymmetry = 1
        else:
            lesion.asymmetry = 2

        lesion.tds = lesion.asymmetry * 1.3
        lesion.tds += lesion.border * 0.1
        lesion.tds += lesion.color_score * 0.5

        if lesion.category == 'Malignant Melanoma':
            result.total_malignant += 1

        if lesion.tds < 3.2 and lesion.category == 'Malignant Melanoma':
            result.false_negatives += 1
        elif lesion.tds > 3.7 and lesion.category != 'Malignant Melanoma':
            result.false_positives += 1
        else:
            result.correct += 1
            if lesion.category == 'Malignant Melanoma':
                result.total_malignant_correct += 1

        result.total += 1

    Results.append(result)



    return render(request, 'border_results/eval.jade', {'Results': Results})
