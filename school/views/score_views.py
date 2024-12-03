from rest_framework import generics
from school.models import Score
from school.serializers import ScoreSerializer

class ScoreList(generics.ListCreateAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def get_queryset(self):
        print(self.request.data)

        queryset = super().get_queryset()
        student_id = self.request.query_params.get("student_id")
        subject = self.request.query_params.get("subject_id")
        score_type = self.request.query_params.get("score_type")
        student_own = self.request.query_params.get("student_own")

        if score_type and score_type == "Quiz" and student_id and subject:
            # filter scores that are quiz for a student in a subject
            queryset = queryset.filter(
                student=student_id, subject=subject, type=score_type
            )

        elif score_type and score_type == "Exam" and subject and not student_own:
            # filter the exam scores of a subject
            queryset = queryset.filter(type=score_type, subject=subject)

        elif score_type and score_type == "Exam" and student_own and student_id:
            # filter exam scores for a student
            queryset = queryset.filter(type=score_type, student=student_id)

        return queryset


class ScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def get_object(self):
        queryset = self.get_queryset()
        student_id = self.request.query_params.get("student_id")
        lesson_id = self.request.query_params.get("lesson_id")
        subject = self.request.query_params.get("subject")
        score_type = self.request.query_params.get("score_type")

        if score_type == "Quiz":
            # get a lesson quiz score for a student
            print("score get")
            obj = generics.get_object_or_404(
                queryset,
                lesson=lesson_id,
                student=student_id,
            )
            return obj
        elif score_type == "Exam":
            # get an exam score for a student in a subject
            obj = generics.get_object_or_404(
                queryset, subject=subject, student=student_id
            )
            return obj
            # print(f"obj {obj}")

