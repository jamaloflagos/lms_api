import random, string
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseBadRequest
from school.models import Applicant
from school.serializers import ApplicantSerializer

User = get_user_model()

class ApplicantList(generics.ListCreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    view_permissions = {
        'get': {'admin': True,},
        'post': {'anon': True,},
    }
    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        contact_mail = serializer.validated_data.get("contact_mail")

        # Check if there is an existing applicant with the same contact_mail or parent_contact_mail
        if Applicant.objects.filter(contact_mail=contact_mail).exists():
            response_message = {"contact_mail": "Email already exists"}
            return HttpResponseBadRequest(response_message)

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        applicant = serializer.save()
        User.objects.create_user(username=applicant.contact_mail, password=password, role='applicant')
        self.send_email(applicant)

    def send_email(self, applicant):
        subject = "New Applicant Created"
        message = f"""
        You have successfully submitted your application, proceed to take your entrance exam with the link beloe

        Link: http://localhost:3000/entrance-exam/{applicant.application_id} 
        """
        recipient_list = [applicant.contact_mail]  # Or any email you want to notify
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


class ApplicantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [AllowAny]
