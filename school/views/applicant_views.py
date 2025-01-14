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

    def perform_create(self, serializer):
        contact_mail = serializer.validated_data.get("contact_mail")

        # Check if there is an existing applicant with the same contact_mail or parent_contact_mail
        if Applicant.objects.filter(contact_mail=contact_mail).exists():
            response_message = {"contact_mail": "Email already exists"}
            return HttpResponseBadRequest(response_message)
        
        if User.objects.filter(email=contact_mail).exists():
            response_message = {"contact_mail": "Email already exists in User records"}
            return HttpResponseBadRequest(response_message)

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        print(password)

        applicant = serializer.save()
        User.objects.create_user(email=applicant.contact_mail, username=f"{applicant.first_name} {applicant.last_name}", password=password, role='Applicant')
        self.send_email(applicant, password)

    def send_email(self, applicant, password):
        subject = "New Applicant Created"
        message = f"""
        You have successfully submitted your application, proceed to take your entrance exam with the link beloe

        Use the credentials below to login to your credentials.
        Email: {applicant.contact_mail}
        Password: {password}
        """
        recipient_list = [applicant.contact_mail]  # Or any email you want to notify
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


class ApplicantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [AllowAny]
