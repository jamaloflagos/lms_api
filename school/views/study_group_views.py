from rest_framework import generics
from django.db.models import Q
from django.shortcuts import get_object_or_404
from school.models import Group, Student, GroupMessage
from school.serializers import GroupSerializer, GroupMessageSerializer, StudentSerializer

class StudyGroupList(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    view_permissions = {
        'get,post': {'student': True}
    }

    def get_queryset(self):
        student_id = self.request.query_params.get('student_id')
        queryset = Group.objects.all()
        if student_id:
            student = Student.objects.filter(pk=student_id).first()
            if student:
                class_members = student._class.students.all()
                queryset = Group.objects.filter(creator__in=class_members)
            else: 
                queryset = Group.objects.none()

        return queryset
    
    def get_serializer_context(self):
        # Add student_id to the serializer context
        context = super().get_serializer_context()
        context["student_id"] = self.request.query_params.get("student_id")
        return context
    
class StudyGroupInfoList(generics.ListAPIView):
    """
    This view
        lists all members of a group
        lists all messages of a group
    """
    view_permissions = {
        'get': {'student': True}
    }

    def get_serializer_class(self):
        data = self.kwargs.get("data")

        if data == "messages":
            return GroupMessageSerializer
        elif data == "members":
            return StudentSerializer

    def get_queryset(self):
        data = self.kwargs.get("data")
        group_id = self.kwargs.get("group_id")
        group = get_object_or_404(Group, pk=group_id)

        if data == "messages":
            return group.messages.all()
        elif data == "members":
            return group.members.all()


class StudyGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    view_permissions = {
        'put,get': {'student': True}
    }
    """
        This view 
            adds a new member to a group
    """

    def perform_update(self, serializer):
        student_id = self.request.data.get('student_id')
        if student_id:
            group_id = self.kwargs["pk"]
            group = Group.objects.filter(id=group_id).first()
            student = Student.objects.filter(id=student_id).first()
            group.members.add(student)

        serializer.save()

class CreateGroupMessage(generics.CreateAPIView):
    queryset = GroupMessage
    serializer_class = GroupMessageSerializer
    view_permissions = {'post': {'student': True}}