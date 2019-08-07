"""antimark URL Configuration"""

from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from .settings import DEBUG

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('poll/', TemplateView.as_view(template_name='poll.html'), name='poll'),
    path('panel/', TemplateView.as_view(template_name='panel.html'), name='panel'),
    path('admin/', admin.site.urls, name='admin')
]

if DEBUG:
    # in DEBUG mode error pages aren't displayed, this allows for working on them even with DEBUG == True
    for error in (404, 500):
        urlpatterns.append(path(f'{error}/', TemplateView.as_view(template_name=f'{error}.html')))
