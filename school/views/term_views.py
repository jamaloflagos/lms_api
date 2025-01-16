from rest_framework import generics
from school.serializers import TermSerializer
from school.models import Term

class CreateTerm(generics.CreateAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    view_permissions = {
        'post': {'admin': True}
    }

class RetrieveTerm(generics.RetrieveAPIView):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    view_permissions = {
        'get': {'admin': True, 'student': True}
    }