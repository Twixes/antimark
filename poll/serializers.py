from rest_framework import serializers
from . import models


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.School
        fields = ('id', 'username', 'name', 'email', 'language', 'nomenclature', 'is_staff', 'is_active', 'joined_at')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        school = serializers.HiddenField(
            default=serializers.CurrentUserDefault()
        )
        model = models.Teacher
        fields = ('id', 'title', 'first_name', 'last_name')


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        school = serializers.HiddenField(
            default=serializers.CurrentUserDefault()
        )
        model = models.Subject
        fields = ('id', 'name', 'name_teacher_selection_case')


class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        school = serializers.HiddenField(
            default=serializers.CurrentUserDefault()
        )
        model = models.StudentGroup
        fields = ('id', 'name', 'number_of_students')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        school = serializers.HiddenField(
            default=serializers.CurrentUserDefault()
        )
        model = models.Question
        fields = ('id', 'position', 'text')


class CompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Completion
        fields = ('student_group', 'added_at')
