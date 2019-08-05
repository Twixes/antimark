from django.contrib import admin
from poll.models import Teacher, Subject, Group, Assignment, Question, Vote

admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Group)
admin.site.register(Assignment)
admin.site.register(Question)
admin.site.register(Vote)
