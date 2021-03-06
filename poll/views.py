from django.http import Http404
from django.shortcuts import render
from django.utils import translation
from django.views import View
from .models import School

class SchoolView(View):
    def get(self, request, username: str):
        try:
            school = School.objects.get(username=username)
        except School.DoesNotExist:
            raise Http404
        context = {
            'school': school
        }
        translation.activate(school.language)
        return render(request, 'school.html', context)


class PollView(View):
    def get(self, request, username: str):
        try:
            school = School.objects.get(username=username)
        except School.DoesNotExist:
            raise Http404
        context = {
            'school': school
        }
        translation.activate(school.language)
        return render(request, 'poll.html', context)
