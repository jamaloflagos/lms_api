from rest_framework import generics
from django.db.models import Q
from django.shortcuts import get_object_or_404
from school.models import StudyGroup, Student
from school.serializers import StudyGroupSerializer, MessageSerializer, StudentSerializer

class StudyGroupList(generics.ListCreateAPIView):
    serializer_class = StudyGroupSerializer
    view_permissions = {
        'get,post': {'student': True}
    }

    def get_queryset(self):
        student_id = self.request.query_params.get('student_id')
        is_member = self.request.query_params.get('is_member')
        queryset = StudyGroup.objects.all()
        if student_id and is_member:
            student = Student.objects.get(pk=student_id)
            if is_member == 'yes':
                queryset = student.study_groups.all()
            elif is_member == 'no':
                class_members = student._class.students.exclude(id=student.id)
                other_classmate_groups = StudyGroup.objects.filter(
                    creator__in=class_members
                ).exclude(Q(students=student) | Q(creator=student))
                queryset = other_classmate_groups

        return queryset
    
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
        data = self.request.query_params.get("data")

        if data == "messages":
            return MessageSerializer
        elif data == "members":
            return StudentSerializer

    def get_queryset(self):
        data = self.kwargs.get("data")
        group_id = self.kwargs.get("group_id")
        group = get_object_or_404(StudyGroup, pk=group_id)

        if data == "messages":
            return group.messages.all()
        elif data == "members":
            return group.students.all()


class StudyGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer
    view_permissions = {
        'put,get': {'student': True}
    }
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
