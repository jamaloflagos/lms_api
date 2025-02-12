import random
import string
from rest_framework import generics
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from school.models import Teacher, ClassSubject, ClassSubjectTeacher
from school.serializers import TeacherSerializer

User = get_user_model()


class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    view_permissions = {
        'post,get': {'admin': True}
    }

    def perform_create(self, serializer):
        # Generate a random password
        print(self.request.data)
        password = "".join(random.choices(string.ascii_letters + string.digits, k=15))
        # Save the teacher instance
        form_class = self.request.data.get('form_class')
        subjects = self.request.data.get('subjects')

        if subjects:
            if form_class:
                teacher = serializer.save()
            else:
                teacher = serializer.save(form_class=None)
            
            for subject in subjects:    
                for class_id in subject['classes_ids']:
                    class_subject = ClassSubject.objects.get(_class=class_id, subject=subject['subject_id'])
                    ClassSubjectTeacher.objects.create(teacher=teacher, class_subject=class_subject)
                    
        User.objects.create_user(id=teacher.id, email=teacher.email, username=f"{teacher.first_name} {teacher.last_name}", password=password, role='Teacher')

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
    view_permissions = {
        'get': {'teacher': True, 'admin': True},
        'put': {'admin': True, 'admin': True},
        'delete': {'admin': True}
    }

