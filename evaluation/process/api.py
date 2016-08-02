from rest_framework import serializers, viewsets
from .models import Process
from .models import ProcessQueue
from .models import ProcessQueueItem
from .models import Algorithm
from .models import Job
from .models import JobStep


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process


class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer


class ProcessQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessQueue


class ProcessQueueViewSet(viewsets.ModelViewSet):
    queryset = ProcessQueue.objects.all()
    serializer_class = ProcessQueueSerializer


class ProcessQueueItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessQueueItem


class ProcessQueueItemViewSet(viewsets.ModelViewSet):
    queryset = ProcessQueueItem.objects.all()
    serializer_class = ProcessQueueItemSerializer


class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm


class AlgorithmViewSet(viewsets.ModelViewSet):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobStep


class JobStepViewSet(viewsets.ModelViewSet):
    queryset = JobStep.objects.all()
    serializer_class = JobStepSerializer
