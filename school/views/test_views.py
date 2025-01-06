from rest_framework import generics
from school.models import UnitTest
from school.serializers import UnitTestSerializer

class UnitTestList(generics.ListCreateAPIView):
    serializer_class = UnitTestSerializer

    def get_queryset(self):
        class_id = self.request.query_params.get('class_id')
        queryset = UnitTest.objects.all()
        if class_id:
            queryset = UnitTest.objects.filter(module__course___class=class_id)
        
        return queryset
    
class UnitTestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnitTest.objects.all()
    serializer_class = UnitTestSerializer