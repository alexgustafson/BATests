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
