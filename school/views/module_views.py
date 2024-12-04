from rest_framework import generics
from school.models import Module
from school.serializers import Moduleserializer

class ModuleList(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = Moduleserializer
    view_permissions = {
        'post': {'teacher': True},
        'get': {'student': True, 'teacher': True}
    }


class ModuleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = Moduleserializer
    view_permissions = {
        'get': {'student': True, 'teacher': True},
        'put,delete': {'teacher': True}
    }
