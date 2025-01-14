from rest_framework import generics
from school.models import Class, Subject
from school.serializers import ClassSerializer

class ClassList(generics.ListCreateAPIView):
    serializer_class = ClassSerializer
    view_permissions = {
        'post': {'admin': True},
        'get': {'teacher': True, 'admin': True, 'student': True, 'anon': True}
    }

    def get_queryset(self):
        queryset = Class.objects.all()
        subject_id = self.request.query_params.get('subject_id')

        if subject_id:
            subject = Subject.objects.get(id=subject_id)
            queryset = Class.objects.filter(class_subjects__subject=subject).distinct()

        return queryset


class ClassDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

