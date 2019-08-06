from django.contrib import admin
from poll.models import Teacher, Subject, Group, Assignment, Question, Completion, Vote


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0


class VoteInline(admin.TabularInline):
    model = Vote
    extra = 0


class GroupAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'number_of_students')
    inlines = [AssignmentInline]


class CompletionAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'added_at')
    inlines = [VoteInline]


admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Group, GroupAdmin)
admin.site.register(Question)
admin.site.register(Completion, CompletionAdmin)
