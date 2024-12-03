from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import Http404
from school.models import Student, Teacher
from school.serializers import StudentSerializer, TeacherSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = JSONParser().parse(request)

        role = data.get("role")
        email = data.get("email")
        password = data.get("password")

        if role == "student":
            print(email, password)
            try:
                student = Student.objects.get(email=email, password=password)
            except Student.DoesNotExist:
                raise Http404

            serializer = StudentSerializer(student)
            return Response(serializer.data)
        elif role == "teacher":
            try:
                teacher = Teacher.objects.get(email=email, password=password)
            except Teacher.DoesNotExist:
                raise Http404

            serializer = TeacherSerializer(teacher)
            return Response({"id": serializer.data["id"]})
