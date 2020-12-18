from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin
from poll import api_views


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()
schools = router.register('schools', api_views.SchoolViewSet)
teachers = schools.register(
    'teachers', api_views.TeacherViewSet, 'teacher', ['school']
)
subjects = schools.register(
    'subjects', api_views.SubjectViewSet, 'subject', ['school']
)
student_groups = schools.register(
    'student-groups', api_views.StudentGroupViewSet, 'student_group', ['school']
)
