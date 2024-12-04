from rest_framework import generics
from django.http import HttpResponseBadRequest
from school.models import Attendance
from school.serializers import AttendanceSerializer

class AttendanceList(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    view_permissions = {
        'post': {'teacher': True},
        'get': {'teacher': True, 'student': True, 'admin': True}
    }

    def perform_create(self, serializer):
        student_id = serializer.validated_data.get("student")
        date_marked = serializer.validated_data.get("data_submitted")

        if Attendance.objects.filter(
            student=student_id, date_marked=date_marked
        ).exists():
            return HttpResponseBadRequest(
                {
                    "detail": "You have already marked an attendance for this student today"
                }
            )

        serializer.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.query_params.get("student_id")

        if student_id:
            queryset = queryset.filter(student=student_id)

        return queryset


class AttendanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    view_permissions = {
        'put,delete': {'teacher': True},
        'get': {'teacher': True, 'admin': True}
    }

