from django.conf.urls import url
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from core import views


urlpatterns = [
    # core
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),
    path('get/events/', views.get_events, name='get_events'),
]
