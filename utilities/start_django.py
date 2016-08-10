import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "evaluation.settings")
django.setup()

print('django loaded')


def startDjango():
    pass