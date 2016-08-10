from __future__ import unicode_literals

from django.conf.urls import url

from .views import CreateProcess
from .views import DeleteProcess
from .views import UpdateProcess
from .views import ListProcess
from .views import ProcessDetail
from .views import Controller

urlpatterns = [
    url(r'^new$', CreateProcess.as_view(), name="process-new"),
    url(r'^edit/(?P<pk>\d+)/$', UpdateProcess.as_view(), name="process-edit"),
    url(r'^detail/(?P<pk>\d+)/$', ProcessDetail.as_view(), name="process-detail"),
    url(r'^delete/(?P<pk>\d+)/$', DeleteProcess.as_view(), name="process-delete"),
    url(r'^$', Controller.as_view(), name="controller"),
]