from rest_framework import generics
from school.models import Module, Class
from school.serializers import Moduleserializer

class ModuleList(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = Moduleserializer
    view_permissions = {
        'post': {'teacher': True},
        'get': {'student': True, 'teacher': True}
    }

    def get_queryset(self):
        class_id = self.request.query_params.get('class_id')
        course_id = self.request.query_params.get('course_id')
        queryset = Module.objects.all()
        if class_id and course_id:
            _class = Class.objects.get(pk=class_id)
            course = _class.courses.get(pk=course_id)
            queryset = course.modules.all()

        return queryset 



class ModuleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = Moduleserializer
    view_permissions = {
        'get': {'student': True, 'teacher': True},
        'put,delete': {'teacher': True}
    }
