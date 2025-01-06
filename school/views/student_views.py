from rest_framework import generics
from school.models import Student
from school.serializers import StudentSerializer

class StudentList(generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    view_permissions = {
        'get': {'teacher': True, 'student': True, 'admin': True}
    }

    def get_queryset(self):
        class_id = self.request.query_params.get('class_id')
        queryset = Student.objects.all()

        if class_id:
            queryset = Student.objects.filter(_class=class_id)

        return queryset
    




class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    view_permissions = {
        'get': {'teacher': True, 'student': True}
    }