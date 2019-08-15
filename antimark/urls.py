"""antimark URL Configuration"""

from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from poll.views import SchoolView, PollView
from .settings import DEBUG

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('panel/', TemplateView.as_view(template_name='panel.html'), name='panel'),
    path('admin/', admin.site.urls, name='admin'),
    path('i18n.js', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('<slug:username>/', SchoolView.as_view(), name='school'),
    path('<slug:username>/poll/', PollView.as_view(), name='poll')
]

if DEBUG:
    # in DEBUG mode error pages aren't displayed, this allows for working on them even in that case
    for error in (404, 500):
        urlpatterns.append(path(f'{error}/', TemplateView.as_view(template_name=f'{error}.html')))
