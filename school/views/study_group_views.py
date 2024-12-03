from rest_framework import generics
from django.shortcuts import get_object_or_404
from school.models import StudyGroup, Student
from school.serializers import StudyGroupSerializer, MessageSerializer, StudentSerializer

class StudyGroupList(generics.ListCreateAPIView):
    """
    This view
        creates a new study group
        lists all study groups
    """

    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer

class StudyGroupInfoList(generics.ListAPIView):
    """
    This view
        lists all members of a group
        lists all messages of a group
    """

    def get_serializer_class(self):
        data_type = self.kwargs.get("data_type")

        if data_type == "messages":
            return MessageSerializer
        elif data_type == "members":
            return StudentSerializer

    def get_queryset(self):
        data_type = self.kwargs.get("data_type")
        group_id = self.kwargs.get("group_id")
        group = get_object_or_404(StudyGroup, pk=group_id)

        if data_type == "messages":
            return group.messages.all()
        elif data_type == "members":
            return group.students.all()


class StudyGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer
    """
        This view 
            adds a new member to a group
    """

    def perform_update(self, serializer):
        student_id = self.kwargs["student_id"]
        group_id = self.kwargs["pk"]
        group = get_object_or_404(StudyGroup, pk=group_id)
        student = get_object_or_404(Student, pk=student_id)
        group.students.add(student)

        serializer.save()
