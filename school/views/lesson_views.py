from rest_framework import generics
from school.models import Lesson, Class
from school.serializers import LessonSerializer

class LessonList(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    view_permissions = {
        'post': {'teacher': True},
        'get': {'teacher': True, 'student': True}
    }


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    view_permissions = {
        'get': {'student': True, 'teacher': True},
        'put,delete': {'teacher': True}
    }

