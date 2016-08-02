from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import serializers
from rest_framework import viewsets

from .models import ProcessResult, Evaluation

class EvaluationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evaluation


class EvaluationViewSet(viewsets.ModelViewSet):

    serializer_class = EvaluationSerializer
    queryset = Evaluation.objects.all()



class ProcessResultLogSerializer(serializers.ModelSerializer):
    evaluation = serializers.PrimaryKeyRelatedField(queryset=Evaluation.objects.all())

    class Meta:
        model = ProcessResult


class ProcessResultViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = ProcessResultLogSerializer
    queryset = ProcessResult.objects.all()

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = ProcessResult.objects.all()
        filename = self.request.query_params.get('filename', None)
        name = self.request.query_params.get('name', None)
        notevaluated = self.request.query_params.get('notevaluated', None)
        if name is not None:
            queryset = queryset.filter(name=name)
        if filename is not None:
            queryset = queryset.filter(json_file=filename)
        if notevaluated is not None:
            queryset = queryset.filter(evaluation__isnull=True)

        return queryset