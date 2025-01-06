from rest_framework import generics
from school.models import Course
from school.serializers import CourseSerializer

class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    view_permissions = {
        'get': {'teacher': True, 'student': True},
        'post': {'teacher': True}
    }

    def get_queryset(self):
        class_id = self.request.query_params.get('class_id')
        creator_id = self.request.query_params.get('creator_id')
        queryset = Course.objects.all()
        if class_id:
            queryset = Course.objects.filter(_class=class_id)
        elif creator_id:
            queryset = Course.objects.filter(creator=class_id)

        return queryset



class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    view_permissions = {
        'get': {'student': True, 'teacher': True, 'admin': True},
        'put,delete': {'teacher': True}
    }
