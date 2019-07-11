from django.conf.urls import url
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from core import views as core_views


urlpatterns = [
    # core
    path('', core_views.index),
    path('index/', core_views.index, name='index'),
    path('get/events/', core_views.get_events, name='get_events'),
]
