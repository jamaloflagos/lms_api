from rest_framework import generics
from school.models import Class
from school.serializers import ClassSerializer

class ClassList(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    view_permissions = {
        'post': {'admin': True},
        'get': {'teacher': True, 'admin': True, 'student': True}
    }


class ClassDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

