import random
import string
from rest_framework import generics
from django.conf import settings
from django.core.mail import send_mail
from school.models import Teacher
from school.serializers import TeacherSerializer

class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def perform_create(self, serializer):
        # Generate a random password
        password = "".join(random.choices(string.ascii_letters + string.digits, k=15))
        # Save the teacher instance
        teacher = serializer.save(password=password)

        # Send an email to the teacher with the password
        send_mail(
            subject="Your Account Has Been Created",
            message=f"""
            Dear {teacher.first_name},

            Your account has been created. Below are your login credentials:

            Email: {teacher.email}
            Password: {password}

            Please log in and change your password as soon as possible.

            Best regards,
            The School Management Team
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[teacher.email],
        )


class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

