from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from . import models, serializers, permissions


class SchoolViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer


class TeacherViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer


class SubjectViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer


class StudentGroupViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = models.StudentGroup.objects.all()
    serializer_class = serializers.StudentGroupSerializer


class QuestionViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer


class CompletionViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = models.Completion.objects.all()
    serializer_class = serializers.CompletionSerializer
    permission_classes = [permissions.IsAuthenticatedAndOwnerOrIsStaff]
