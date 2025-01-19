from rest_framework import generics
from school.models import EntranceExamQuestion, EntranceExamScore
from school.serializers import EntranceExamQuestionSerializer, EntranceExamScoreSerializer

class EntranceExamQuestionList(generics.ListCreateAPIView):
    queryset = EntranceExamQuestion.objects.all()
    serializer_class = EntranceExamQuestionSerializer
    view_permissions = {
        'get': {'applicant': True} 
    }


class EntranceExamScoreList(generics.ListCreateAPIView):
    queryset = EntranceExamScore.objects.all()
    serializer_class = EntranceExamScoreSerializer
    view_permissions = {
        'post': {'applicant': True} 
    }


class EntranceExamScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EntranceExamScore.objects.all()
    serializer_class = EntranceExamScoreSerializer
    view_permissions = {
        'get': {'applicant': True}
    }

    def get_object(self):
        queryset = self.get_queryset()
        applicant_id = self.kwargs.get("applicant_id")

        obj = generics.get_object_or_404(queryset, applicant_id=applicant_id)
        return obj

class QuestionList(generics.ListCreateAPIView):
    queryset = EntranceExamQuestion.objects.all()
    serializer_class = EntranceExamQuestionSerializer


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EntranceExamQuestion.objects.all()
    serializer_class = EntranceExamQuestionSerializer
