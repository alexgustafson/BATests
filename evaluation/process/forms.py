from django import forms
from .models import Process


class ProcessForm(forms.ModelForm):

    class Meta:
        model = Process
