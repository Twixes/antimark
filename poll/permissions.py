from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import School, Teacher, Subject, StudentGroup, Assignment, Question, Completion, Vote


class IsAuthenticatedAndOwnerOrIsStaffOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            elif isinstance(obj, School):
                return request.user.id == obj.id
            elif isinstance(obj, Vote):
                return request.user.id == obj.completion.school.id
            else:
                return request.user.id == obj.school.id
        else:
            return request.method in SAFE_METHODS


class IsAuthenticatedAndOwnerOrIsStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            elif isinstance(obj, School):
                return request.user.id == obj.id
            elif isinstance(obj, Vote):
                return request.user.id == obj.completion.school.id
            else:
                return request.user.id == obj.school.id
        else:
            return False
