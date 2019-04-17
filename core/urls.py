from django.conf.urls import url
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView


urlpatterns = [
    # core
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),
]
