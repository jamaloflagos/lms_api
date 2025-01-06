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

    def get_queryset(self):
        class_id = self.request.query_params.get('class_id')
        course_id = self.request.query_params.get('course_id')
        module_id = self.request.query_params.get('module_id')
        queryset = Lesson.objects.all()
        if class_id and course_id and module_id:
            _class = Class.objects.get(pk=class_id)
            course = _class.courses.get(pk=course_id)
            module = course.modules.get(pk=module_id)
            queryset = module.lessons.all()

        return queryset

class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    view_permissions = {
        'get': {'student': True, 'teacher': True},
        'put,delete': {'teacher': True}
    }

