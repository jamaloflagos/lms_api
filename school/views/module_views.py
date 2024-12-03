from rest_framework import generics
from school.models import Module
from school.serializers import Moduleserializer

class ModuleList(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = Moduleserializer


class ModuleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = Moduleserializer

