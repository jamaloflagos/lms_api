from rest_framework import generics
from school.models import Exam
from school.serializers import ExamSerializer

class ExamList(generics.ListCreateAPIView):
    serializer_class = ExamSerializer

    def get_queryset(self):
        class_id = self.request.query_params.get('class_id')
        queryset = Exam.objects.all()
        if class_id:
            queryset = Exam.objects.filter(course___class=class_id)
        
        return queryset
    
class ExamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer