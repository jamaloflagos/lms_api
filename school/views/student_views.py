from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.db.models import Q
from school.models import Student, Score, StudyGroup
from school.serializers import StudentSerializer, ScoreSerializer, StudyGroupSerializer

class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentInfoList(generics.ListAPIView):
    """
    This view
        lists all of the scores obtained by a student
        lists all groups related to a student
    """
    view_permissions = {
        'get': {'teacher': True, 'student': True}
    }

    def get_serializer_class(self):
        data_type = self.kwargs.get("data_type")

        if data_type == "scores":
            return ScoreSerializer
        else:
            return StudyGroupSerializer

    def get_queryset(self):
        student_id = self.kwargs.get("student_id")
        data_type = self.kwargs.get("data_type")
        status = self.request.query_params.get("status")

        if data_type == "scores":
            return Score.objects.filter(student=student_id)
        elif data_type == "groups":
            student = get_object_or_404(Student, pk=student_id)

            if status == "member":
                # student = get_object_or_404(Student, pk=student_id)
                return student.study_groups.all()
            elif status == "non-member":
                # Groups created by other students in the same class
                class_members = student._class.students.exclude(id=student.id)
                other_classmate_groups = StudyGroup.objects.filter(
                    creator__in=class_members
                ).exclude(Q(students=student) | Q(creator=student))

                return other_classmate_groups

        else:
            return Student.objects.all()

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    view_permissions = {
        'get': {'teacher': True, 'student': True}
    }