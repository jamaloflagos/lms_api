from rest_framework import generics
from school.models import Lesson, Class
from school.serializers import LessonSerializer

class LessonList(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        _class = serializer.validated_data.get("_class")
        class_instance = Class.objects.get(name=_class)
        serializer.save(_class=class_instance)

    def get_queryset(self):
        queryset = super().get_queryset()
        class_id = self.request.query_params.get("class_id")
        subject = self.request.query_params.get("subject")
        teacher_id = self.request.query_params.get("teacher_id")

        if class_id and subject:
            queryset = queryset.filter(_class=class_id, subject=subject)

        elif teacher_id and subject:
            queryset = queryset.filter(teacher=teacher_id, subject=subject)

        return queryset


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

