from rest_framework import generics
from school.models import ClassSchedule
from school.serializers import ClassScheduleSerializer

class ScheduleList(generics.ListCreateAPIView):
    serializer_class = ClassScheduleSerializer

    def get_queryset(self):
        class_id = self.request.query_params.get('class_id')
        queryset = ClassSchedule.objects.all()
        if class_id:
            queryset = ClassSchedule.objects.filter(course___class=class_id)

        return queryset
    
class ScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassSchedule.objects.all()
    serializer_class = ClassScheduleSerializer