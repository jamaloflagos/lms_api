from rest_framework import generics
from school.models import Course
from school.serializers import CourseSerializer

class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    view_permissions = {
        'post': {'teacher': True}
    }


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    view_permissions = {
        'get': {'student': True, 'teacher': True, 'admin': True},
        'put,delete': {'teacher': True}
    }
