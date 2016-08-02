"""evaluation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from border_results.api import ProcessResultViewSet, EvaluationViewSet

from process.api import ProcessViewSet
from process.api import ProcessQueueViewSet
from process.api import ProcessQueueItemViewSet
from process.api import AlgorithmViewSet
from process.api import JobViewSet
from process.api import JobStepViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'processlog', ProcessResultViewSet)
router.register(r'evaluation', EvaluationViewSet)
router.register(r'process', ProcessViewSet)
router.register(r'processqueue', ProcessQueueViewSet)
router.register(r'processqueueitem', ProcessQueueItemViewSet)
router.register(r'algorithm', AlgorithmViewSet)
router.register(r'job', JobViewSet)
router.register(r'jobstep', JobStepViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^borders', 'border_results.views.index'),
    url(r'^initialize', 'border_results.views.initialize'),
    url(r'^process', include('process.urls', namespace='process')),
    url(r'^api/processlogs/$', 'border_results.views.processlogs'),
    #url(r'^', 'border_results.views.index'),
]


